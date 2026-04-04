"""
Agent Team — the four specialized agents working simultaneously.

Arthur (Chief of Staff) — coordinates and delegates
Ariadne (CTO) — technical decisions and code
Eames (CMO) — marketing and content
Yusuf (COO) — operations and analytics
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass

from agents.base_agent import BaseAgent, TaskResult
from router.model_router import ModelRouter, TaskComplexity

logger = logging.getLogger(__name__)


@dataclass
class TeamResult:
    """Result from a team-coordinated task."""
    original_task: str
    delegations: list[TaskResult]
    summary: str


class AgentTeam:
    """Manages the four agents and enables simultaneous work."""

    def __init__(self, router: ModelRouter) -> None:
        self.router = router
        self.arthur = BaseAgent("arthur", router)
        self.ariadne = BaseAgent("ariadne", router)
        self.eames = BaseAgent("eames", router)
        self.yusuf = BaseAgent("yusuf", router)

        self._agents = {
            "arthur": self.arthur,
            "ariadne": self.ariadne,
            "eames": self.eames,
            "yusuf": self.yusuf,
        }

    def get_agent(self, name: str) -> BaseAgent:
        agent = self._agents.get(name.lower())
        if not agent:
            raise ValueError(f"Unknown agent: {name}. Available: {list(self._agents)}")
        return agent

    async def delegate(self, task: str, context: str = "") -> TeamResult:
        """
        Arthur analyzes the task and delegates to the right agent(s).
        Multiple agents can work simultaneously on different subtasks.
        """
        # Step 1: Arthur decides who should handle what
        routing_prompt = (
            f"Analyze this task and decide which team member(s) should handle it.\n"
            f"Team members:\n"
            f"- ariadne (CTO): technical, code, architecture, engineering\n"
            f"- eames (CMO): marketing, content, copywriting, brand\n"
            f"- yusuf (COO): operations, data analysis, process, logistics\n\n"
            f"Respond in JSON format:\n"
            f'{{"delegations": [{{"agent": "name", "subtask": "description"}}]}}\n\n'
            f"Task: {task}"
        )

        routing_result = await self.arthur.handle_task(
            routing_prompt, context, TaskComplexity.LOW
        )

        # Step 2: Parse delegations and run simultaneously
        delegations = self._parse_delegations(routing_result.response)

        if not delegations:
            # If Arthur can't parse, default to most relevant agent
            result = await self.ariadne.handle_task(task, context)
            return TeamResult(
                original_task=task,
                delegations=[result],
                summary=result.response,
            )

        # Step 3: Run all delegated tasks simultaneously
        tasks = []
        for agent_name, subtask in delegations:
            agent = self._agents.get(agent_name, self.ariadne)
            tasks.append(agent.handle_task(subtask, context))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Collect successful results
        task_results: list[TaskResult] = []
        for r in results:
            if isinstance(r, TaskResult):
                task_results.append(r)
            else:
                logger.error("Agent task failed: %s", r)

        # Step 4: Arthur summarizes if multiple agents worked
        summary = ""
        if len(task_results) == 1:
            summary = task_results[0].response
        elif task_results:
            combined = "\n\n".join(
                f"[{r.agent_name}]: {r.response}" for r in task_results
            )
            summary_result = await self.arthur.handle_task(
                f"Summarize these team responses into a cohesive answer:\n\n{combined}",
                complexity=TaskComplexity.LOW,
            )
            summary = summary_result.response

        return TeamResult(
            original_task=task,
            delegations=task_results,
            summary=summary,
        )

    async def direct(
        self, agent_name: str, task: str, context: str = ""
    ) -> TaskResult:
        """Send a task directly to a specific agent, bypassing Arthur."""
        agent = self.get_agent(agent_name)
        return await agent.handle_task(task, context)

    def _parse_delegations(self, response: str) -> list[tuple[str, str]]:
        """Parse Arthur's routing JSON response."""
        import json
        try:
            # Find JSON in the response
            start = response.find("{")
            end = response.rfind("}") + 1
            if start == -1 or end == 0:
                return []
            data = json.loads(response[start:end])
            return [
                (d["agent"].lower(), d["subtask"])
                for d in data.get("delegations", [])
                if d.get("agent", "").lower() in self._agents
            ]
        except (json.JSONDecodeError, KeyError):
            return []
