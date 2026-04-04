"""
Telegram Bot — communication channel for the agent team.
"""

from __future__ import annotations

import asyncio
import logging
import os

logger = logging.getLogger(__name__)

try:
    from telegram import Update
    from telegram.ext import (
        Application,
        CommandHandler,
        MessageHandler,
        ContextTypes,
        filters,
    )

    HAS_TELEGRAM = True
except ImportError:
    HAS_TELEGRAM = False


class TelegramBot:
    """Telegram interface for the Claude Code agent team."""

    def __init__(self, on_message=None) -> None:
        if not HAS_TELEGRAM:
            raise ImportError(
                "python-telegram-bot is required. Install with: "
                "pip install python-telegram-bot"
            )

        token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
        if not token:
            raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set")

        self._on_message = on_message
        self.app = Application.builder().token(token).build()
        self._setup_handlers()

    def _setup_handlers(self) -> None:
        self.app.add_handler(CommandHandler("start", self._cmd_start))
        self.app.add_handler(CommandHandler("status", self._cmd_status))
        self.app.add_handler(CommandHandler("ask", self._cmd_ask))
        self.app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_message)
        )

    async def _cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "Claude Code Agents ready.\n\n"
            "Send any message to interact with the team.\n"
            "Use /ask <agent> <question> to ask a specific agent.\n"
            "Use /status to check system status."
        )

    async def _cmd_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if self._on_message:
            response = await self._on_message(
                text="/status",
                user=str(update.effective_user.id),
                channel="telegram",
                metadata={"chat_id": update.effective_chat.id},
            )
            await update.message.reply_text(response or "System running.")

    async def _cmd_ask(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text.replace("/ask", "", 1).strip()
        if self._on_message:
            response = await self._on_message(
                text=text,
                user=str(update.effective_user.id),
                channel="telegram",
                metadata={
                    "chat_id": update.effective_chat.id,
                    "direct_agent": True,
                },
            )
            if response:
                await update.message.reply_text(response)

    async def _handle_message(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        text = update.message.text
        user = str(update.effective_user.id)

        logger.info("[Telegram] Message from %s: %s", user, text[:80])

        if self._on_message:
            response = await self._on_message(
                text=text,
                user=user,
                channel="telegram",
                metadata={"chat_id": update.effective_chat.id},
            )
            if response:
                await update.message.reply_text(response)

    async def start(self) -> None:
        await self.app.initialize()
        await self.app.start()
        await self.app.updater.start_polling()
        logger.info("Telegram bot started")

    async def stop(self) -> None:
        await self.app.updater.stop()
        await self.app.stop()
        await self.app.shutdown()
