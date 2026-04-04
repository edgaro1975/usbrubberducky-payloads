#!/usr/bin/env python3
"""
Claude Code Agents — Multi-Agent AI System
Powered by Claude Code (replacing OpenClaw)

Usage:
    python main.py                  # Start with all comm channels
    python main.py --cli            # Interactive CLI mode
    python main.py --ask "question" # One-shot question

Environment variables:
    ANTHROPIC_API_KEY       — Required for Claude models
    GOOGLE_API_KEY          — Optional, for Gemini
    GROQ_API_KEY            — Optional, for Groq
    SLACK_BOT_TOKEN         — Optional, enables Slack
    SLACK_APP_TOKEN         — Optional, for Slack Socket Mode
    TELEGRAM_BOT_TOKEN      — Optional, enables Telegram
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import signal
import sys

from orchestrator import Orchestrator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("claude-agents")

BANNER = r"""
  _____ _                 _         ____          _
 / ____| |               | |       / ___|___   __| | ___
| |    | | __ _ _   _  __| | ___  | |   / _ \ / _` |/ _ \
| |    | |/ _` | | | |/ _` |/ _ \ | |__| (_) | (_| |  __/
|_|____|_|\__,_|\__,_|\__,_|\___| _\____\___/ \__,_|\___|
    / \   __ _  ___ _ __ | |_ ___
   / _ \ / _` |/ _ \ '_ \| __/ __|
  / ___ \ (_| |  __/ | | | |_\__ \
 /_/   \_\__, |\___|_| |_|\__|___/
         |___/

  Arthur (Chief of Staff) | Ariadne (CTO)
  Eames (CMO)             | Yusuf (COO)

  Powered by Claude Code — replacing OpenClaw
"""


async def cli_mode(orchestrator: Orchestrator) -> None:
    """Interactive CLI for chatting with the agent team."""
    print(BANNER)
    print("Type a message to interact with the team.")
    print("Prefix with @agent_name to talk to a specific agent.")
    print("Commands: /status, /agents, /history, /quit\n")

    loop = asyncio.get_event_loop()

    while True:
        try:
            user_input = await loop.run_in_executor(None, lambda: input("You> "))
        except (EOFError, KeyboardInterrupt):
            break

        if not user_input.strip():
            continue
        if user_input.strip().lower() in ("/quit", "/exit", "quit", "exit"):
            break

        response = await orchestrator.handle_message(
            text=user_input, user="cli_user", channel="cli"
        )
        print(f"\n{response}\n")


async def one_shot(orchestrator: Orchestrator, question: str) -> None:
    """Ask a single question and print the response."""
    response = await orchestrator.handle_message(
        text=question, user="cli_user", channel="cli"
    )
    print(response)


async def run_server(orchestrator: Orchestrator) -> None:
    """Run as a long-lived server with communication channels."""
    print(BANNER)
    logger.info("Running in server mode — waiting for messages...")

    stop_event = asyncio.Event()

    def _signal_handler():
        stop_event.set()

    loop = asyncio.get_event_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, _signal_handler)

    await stop_event.wait()


async def main() -> None:
    parser = argparse.ArgumentParser(description="Claude Code Agents")
    parser.add_argument("--cli", action="store_true", help="Interactive CLI mode")
    parser.add_argument("--ask", type=str, help="One-shot question")
    args = parser.parse_args()

    orchestrator = Orchestrator()
    await orchestrator.start()

    try:
        if args.ask:
            await one_shot(orchestrator, args.ask)
        elif args.cli:
            await cli_mode(orchestrator)
        else:
            await run_server(orchestrator)
    finally:
        await orchestrator.stop()


if __name__ == "__main__":
    asyncio.run(main())
