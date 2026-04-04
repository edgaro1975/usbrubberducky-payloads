"""
Base Agent — foundation for all specialized AI agents.

Each agent has:
- A role and system prompt
- A preferred model (routed via ModelRouter)
- Persistent task-specific memory
- Ability to work simultaneously with other agents
"""

from __future__ import annotations

import json
import logging
import os
import time
from dataclasses import dataclass, field
from pathlib import Path

from config import AGENTS, MEMORY_DIR, AgentConfig
from router.model_router import ModelRouter, TaskComplexity

logger = logging.getLogger(__name__)


@dataclass
class TaskResult:
    agent_name: str
    task: str
    response: str
    model_used: str
    elapsed_ms: float
    success: bool
    error: str = ""


class BaseAgent:
    """A specialized AI agent that focuses on one area for all tasks."""

    def __init__(self, agent_key: str, router: ModelRouter) -> None:
        if agent_key not in AGENTS:
            raise ValueError(f"Unknown agent: {agent_key}")

        self.key = agent_key
        self.config: AgentConfig = AGENTS[agent_key]
        self.router = router
        self.memory: list[dict] = []
        self.memory_path = Path(MEMORY_DIR) / f"{agent_key}_memory.json"
        self._load_memory()

    @property
    def name(self) -> str:
        return self.config.name

    @property
    def role(self) -> str:
        return self.config.role

    async def handle_task(
        self,
        task: str,
        context: str = "",
        complexity: TaskComplexity = TaskComplexity.MEDIUM,
    ) -> TaskResult:
        """Process a task and return the result."""
        start = time.monotonic()

        # Build conversation with memory context
        messages = self._build_messages(task, context)

        # Route to the best model
        decision = self.router.route(self.config.preferred_model, complexity)
        logger.info(
            "[%s] Handling task via %s (%s): %s",
            self.name, decision.model_id, decision.reason, task[:80],
        )

        try:
            response = await self.router.send(
                model_key=self._find_model_key(decision.model_id),
                messages=messages,
                system=self.config.system_prompt,
            )

            # Save to memory
            self._add_to_memory(task, response)

            elapsed = (time.monotonic() - start) * 1000
            return TaskResult(
                agent_name=self.name,
                task=task,
                response=response,
                model_used=decision.model_id,
                elapsed_ms=elapsed,
                success=True,
            )

        except Exception as e:
            elapsed = (time.monotonic() - start) * 1000
            logger.error("[%s] Task failed: %s", self.name, e)
            return TaskResult(
                agent_name=self.name,
                task=task,
                response="",
                model_used=decision.model_id,
                elapsed_ms=elapsed,
                success=False,
                error=str(e),
            )

    def _build_messages(self, task: str, context: str) -> list[dict]:
        """Build the message list including relevant memory."""
        messages: list[dict] = []

        # Include recent memory for continuity
        for mem in self.memory[-5:]:
            messages.append({"role": "user", "content": mem["task"]})
            messages.append({"role": "assistant", "content": mem["response"]})

        # Current task
        content = task
        if context:
            content = f"Context:\n{context}\n\nTask:\n{task}"
        messages.append({"role": "user", "content": content})

        return messages

    def _add_to_memory(self, task: str, response: str) -> None:
        self.memory.append({
            "task": task,
            "response": response[:500],  # truncate for storage
            "timestamp": time.time(),
        })
        # Keep memory bounded
        if len(self.memory) > 100:
            self.memory = self.memory[-50:]
        self._save_memory()

    def _load_memory(self) -> None:
        if self.memory_path.exists():
            try:
                self.memory = json.loads(self.memory_path.read_text())
            except (json.JSONDecodeError, OSError):
                self.memory = []

    def _save_memory(self) -> None:
        self.memory_path.parent.mkdir(parents=True, exist_ok=True)
        self.memory_path.write_text(json.dumps(self.memory, indent=2))

    def _find_model_key(self, model_id: str) -> str:
        """Find the config key for a given model_id."""
        for key, cfg in self.router.models.items():
            if cfg.model_id == model_id:
                return key
        raise ValueError(f"Model not found in router: {model_id}")

    def clear_memory(self) -> None:
        self.memory = []
        if self.memory_path.exists():
            self.memory_path.unlink()

    def __repr__(self) -> str:
        return f"<Agent {self.name} ({self.role})>"
