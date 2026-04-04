"""
Memory Store — persistent storage for agent memories and task history.

Stores data locally (replaces the 6TB RAID / NAS from the architecture).
"""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path
from dataclasses import dataclass, asdict

from config import MEMORY_DIR, LOGS_DIR

logger = logging.getLogger(__name__)


@dataclass
class TaskLog:
    timestamp: float
    agent: str
    task: str
    response_preview: str
    model_used: str
    elapsed_ms: float
    success: bool
    channel: str = ""
    user: str = ""


class MemoryStore:
    """Manages persistent storage for the agent system."""

    def __init__(self) -> None:
        self.memory_dir = Path(MEMORY_DIR)
        self.logs_dir = Path(LOGS_DIR)
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self._task_log: list[TaskLog] = []
        self._load_task_log()

    def log_task(self, log: TaskLog) -> None:
        self._task_log.append(log)
        self._save_task_log()

    def get_recent_tasks(self, n: int = 20) -> list[TaskLog]:
        return self._task_log[-n:]

    def get_agent_tasks(self, agent: str, n: int = 20) -> list[TaskLog]:
        return [t for t in self._task_log if t.agent == agent][-n:]

    def get_stats(self) -> dict:
        total = len(self._task_log)
        if total == 0:
            return {"total_tasks": 0}

        successful = sum(1 for t in self._task_log if t.success)
        agents = {}
        for t in self._task_log:
            agents.setdefault(t.agent, {"count": 0, "success": 0})
            agents[t.agent]["count"] += 1
            if t.success:
                agents[t.agent]["success"] += 1

        return {
            "total_tasks": total,
            "success_rate": successful / total,
            "agents": agents,
        }

    def _load_task_log(self) -> None:
        log_file = self.logs_dir / "task_log.json"
        if log_file.exists():
            try:
                data = json.loads(log_file.read_text())
                self._task_log = [TaskLog(**entry) for entry in data]
            except (json.JSONDecodeError, TypeError):
                self._task_log = []

    def _save_task_log(self) -> None:
        log_file = self.logs_dir / "task_log.json"
        data = [asdict(t) for t in self._task_log[-1000:]]  # keep last 1000
        log_file.write_text(json.dumps(data, indent=2))
