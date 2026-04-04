"""
Orchestrator — the main brain of the Claude Code Agents system.

Replaces OpenClaw's core with Claude Code as the backbone.
Connects: Router <-> Agents <-> Communication Channels <-> Storage
"""

from __future__ import annotations

import asyncio
import logging
import time

from agents.base_agent import TaskResult
from agents.team import AgentTeam
from router.model_router import ModelRouter, TaskComplexity
from storage.memory_store import MemoryStore, TaskLog
from watchdog import Watchdog

logger = logging.getLogger(__name__)


class Orchestrator:
    """
    Central orchestrator that ties everything together:
    - Receives messages from communication channels
    - Routes them through the agent team
    - Stores results in memory
    - Monitors system health via watchdog
    """

    def __init__(self) -> None:
        self.router = ModelRouter()
        self.team = AgentTeam(self.router)
        self.store = MemoryStore()
        self.watchdog = Watchdog(self.router)
        self._comms: list = []

    async def start(self) -> None:
        """Initialize all subsystems."""
        logger.info("Starting Claude Code Agents orchestrator...")

        # Start the model router
        await self.router.start()

        # Start the watchdog
        await self.watchdog.start()

        # Start communication channels
        await self._start_comms()

        logger.info("Orchestrator ready — all systems online")

    async def stop(self) -> None:
        """Gracefully shut down all subsystems."""
        logger.info("Shutting down orchestrator...")
        await self.watchdog.stop()
        for comm in self._comms:
            await comm.stop()
        await self.router.stop()
        logger.info("Orchestrator stopped")

    async def handle_message(
        self,
        text: str,
        user: str = "",
        channel: str = "",
        metadata: dict | None = None,
    ) -> str:
        """
        Main entry point for all incoming messages.
        Called by communication channels (Slack, Telegram, CLI).
        """
        metadata = metadata or {}

        # Handle system commands
        if text.startswith("/"):
            return await self._handle_command(text, user)

        # Determine complexity from message length and content
        complexity = self._assess_complexity(text)

        # Check if message targets a specific agent
        agent_name = self._extract_agent_target(text)

        if agent_name:
            # Direct to specific agent
            clean_text = self._remove_agent_prefix(text, agent_name)
            result = await self.team.direct(agent_name, clean_text)
            self._log_result(result, channel, user)
            return f"**[{result.agent_name}]**: {result.response}"
        else:
            # Let Arthur coordinate the team
            team_result = await self.team.delegate(text)
            for r in team_result.delegations:
                self._log_result(r, channel, user)
            return team_result.summary

    async def _handle_command(self, text: str, user: str) -> str:
        cmd = text.split()[0].lower()

        if cmd == "/status":
            health = self.watchdog.get_status()
            stats = self.store.get_stats()
            models = health.get("models", {})
            available = sum(1 for v in models.values() if v)
            return (
                f"**Claude Code Agents Status**\n"
                f"Models: {available}/{len(models)} available\n"
                f"Tasks completed: {stats.get('total_tasks', 0)}\n"
                f"Success rate: {stats.get('success_rate', 0):.0%}\n"
                f"Issues: {', '.join(health.get('issues', [])) or 'None'}"
            )

        if cmd == "/agents":
            lines = []
            for key, agent in self.team._agents.items():
                lines.append(f"- **{agent.name}** ({agent.role})")
            return "**Active Agents:**\n" + "\n".join(lines)

        if cmd == "/history":
            recent = self.store.get_recent_tasks(10)
            if not recent:
                return "No task history yet."
            lines = []
            for t in recent:
                status = "OK" if t.success else "FAIL"
                lines.append(
                    f"[{status}] {t.agent}: {t.task[:60]}... ({t.elapsed_ms:.0f}ms)"
                )
            return "**Recent Tasks:**\n" + "\n".join(lines)

        return f"Unknown command: {cmd}. Available: /status, /agents, /history"

    def _assess_complexity(self, text: str) -> TaskComplexity:
        length = len(text)
        keywords_high = ["architect", "design", "refactor", "analyze", "strategy"]
        keywords_critical = ["urgent", "critical", "production", "security"]

        if any(k in text.lower() for k in keywords_critical):
            return TaskComplexity.CRITICAL
        if any(k in text.lower() for k in keywords_high) or length > 500:
            return TaskComplexity.HIGH
        if length > 100:
            return TaskComplexity.MEDIUM
        return TaskComplexity.LOW

    def _extract_agent_target(self, text: str) -> str | None:
        """Check if message starts with @agent_name."""
        lower = text.lower().strip()
        for name in self.team._agents:
            if lower.startswith(f"@{name}"):
                return name
        return None

    def _remove_agent_prefix(self, text: str, agent_name: str) -> str:
        lower = text.lower().strip()
        if lower.startswith(f"@{agent_name}"):
            return text[len(agent_name) + 1:].strip()
        return text

    def _log_result(self, result: TaskResult, channel: str, user: str) -> None:
        self.store.log_task(TaskLog(
            timestamp=time.time(),
            agent=result.agent_name,
            task=result.task[:200],
            response_preview=result.response[:200],
            model_used=result.model_used,
            elapsed_ms=result.elapsed_ms,
            success=result.success,
            channel=channel,
            user=user,
        ))

    async def _start_comms(self) -> None:
        """Start available communication channels."""
        import os

        # Try Slack
        if os.environ.get("SLACK_BOT_TOKEN"):
            try:
                from comms.slack_bot import SlackBot
                slack = SlackBot(on_message=self.handle_message)
                await slack.start()
                self._comms.append(slack)
                logger.info("Slack bot connected")
            except (ImportError, Exception) as e:
                logger.info("Slack not available: %s", e)

        # Try Telegram
        if os.environ.get("TELEGRAM_BOT_TOKEN"):
            try:
                from comms.telegram_bot import TelegramBot
                telegram = TelegramBot(on_message=self.handle_message)
                await telegram.start()
                self._comms.append(telegram)
                logger.info("Telegram bot connected")
            except (ImportError, Exception) as e:
                logger.info("Telegram not available: %s", e)
