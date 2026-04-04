"""
Slack Bot — communication channel for the agent team.

Uses Slack's Socket Mode for real-time messaging.
"""

from __future__ import annotations

import asyncio
import logging
import os

logger = logging.getLogger(__name__)

try:
    from slack_bolt.async_app import AsyncApp
    from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler

    HAS_SLACK = True
except ImportError:
    HAS_SLACK = False


class SlackBot:
    """Slack interface for the Claude Code agent team."""

    def __init__(self, on_message=None) -> None:
        if not HAS_SLACK:
            raise ImportError(
                "slack_bolt is required. Install with: pip install slack-bolt"
            )

        self.app = AsyncApp(
            token=os.environ.get("SLACK_BOT_TOKEN", ""),
            name="Claude Code Agents",
        )
        self._on_message = on_message
        self._handler: AsyncSocketModeHandler | None = None
        self._setup_handlers()

    def _setup_handlers(self) -> None:
        @self.app.event("message")
        async def handle_message(event, say):
            text = event.get("text", "")
            user = event.get("user", "unknown")
            channel = event.get("channel", "")

            if not text or event.get("bot_id"):
                return

            logger.info("[Slack] Message from %s: %s", user, text[:80])

            if self._on_message:
                response = await self._on_message(
                    text=text,
                    user=user,
                    channel="slack",
                    metadata={"slack_channel": channel},
                )
                if response:
                    await say(response)

        @self.app.event("app_mention")
        async def handle_mention(event, say):
            text = event.get("text", "")
            user = event.get("user", "unknown")
            channel = event.get("channel", "")

            if self._on_message:
                response = await self._on_message(
                    text=text,
                    user=user,
                    channel="slack",
                    metadata={"slack_channel": channel, "mention": True},
                )
                if response:
                    await say(response)

    async def start(self) -> None:
        app_token = os.environ.get("SLACK_APP_TOKEN", "")
        if not app_token:
            logger.warning("SLACK_APP_TOKEN not set — Slack bot disabled")
            return
        self._handler = AsyncSocketModeHandler(self.app, app_token)
        await self._handler.start_async()
        logger.info("Slack bot started")

    async def stop(self) -> None:
        if self._handler:
            await self._handler.close_async()

    async def send_message(self, channel: str, text: str) -> None:
        await self.app.client.chat_postMessage(channel=channel, text=text)
