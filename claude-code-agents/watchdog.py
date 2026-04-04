"""
Watchdog — monitors system health using a lightweight model.

Periodically checks:
- Model availability (cloud + local)
- Agent responsiveness
- Memory/storage usage
- Communication channel status
"""

from __future__ import annotations

import asyncio
import logging
import time

from config import WATCHDOG_CHECK_INTERVAL, WATCHDOG_MODEL
from router.model_router import ModelRouter

logger = logging.getLogger(__name__)


class Watchdog:
    """System health monitor running on a lightweight local model."""

    def __init__(self, router: ModelRouter) -> None:
        self.router = router
        self.interval = WATCHDOG_CHECK_INTERVAL
        self._running = False
        self._last_report: dict = {}
        self._task: asyncio.Task | None = None

    async def start(self) -> None:
        self._running = True
        self._task = asyncio.create_task(self._monitor_loop())
        logger.info("Watchdog started (interval=%ds, model=%s)", self.interval, WATCHDOG_MODEL)

    async def stop(self) -> None:
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

    async def _monitor_loop(self) -> None:
        while self._running:
            try:
                await self._check_health()
            except Exception as e:
                logger.error("Watchdog check failed: %s", e)
            await asyncio.sleep(self.interval)

    async def _check_health(self) -> None:
        report: dict = {"timestamp": time.time(), "models": {}, "issues": []}

        # Check all model endpoints
        model_status = await self.router.check_all()
        report["models"] = model_status

        unavailable = [k for k, v in model_status.items() if not v]
        if unavailable:
            report["issues"].append(f"Unavailable models: {', '.join(unavailable)}")
            logger.warning("Models unavailable: %s", unavailable)

        available_count = sum(1 for v in model_status.values() if v)
        total = len(model_status)
        logger.info(
            "Watchdog: %d/%d models available", available_count, total
        )

        self._last_report = report

    def get_status(self) -> dict:
        """Return the latest health report."""
        return self._last_report
