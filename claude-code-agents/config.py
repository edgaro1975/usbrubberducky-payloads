"""
Claude Code Agents — Configuration
Replaces OpenClaw with Claude Code-powered multi-agent architecture.
"""

import os
from dataclasses import dataclass, field


@dataclass
class ModelConfig:
    """Configuration for a single model endpoint."""
    model_id: str
    provider: str  # "anthropic", "google", "groq", "ollama"
    api_key_env: str = ""
    base_url: str = ""
    max_tokens: int = 4096
    temperature: float = 0.7

    @property
    def api_key(self) -> str:
        if self.api_key_env:
            return os.environ.get(self.api_key_env, "")
        return ""


@dataclass
class AgentConfig:
    """Configuration for a specialized AI agent."""
    name: str
    role: str
    description: str
    preferred_model: str  # model_id to use
    memory_path: str = ""
    system_prompt: str = ""


@dataclass
class CommsConfig:
    """Communication channel configuration."""
    slack_token_env: str = "SLACK_BOT_TOKEN"
    slack_app_token_env: str = "SLACK_APP_TOKEN"
    telegram_token_env: str = "TELEGRAM_BOT_TOKEN"
    enabled_channels: list[str] = field(default_factory=lambda: ["slack", "telegram"])


# ---------------------------------------------------------------------------
# Cloud Models (replacing OpenClaw's cloud model config)
# ---------------------------------------------------------------------------
CLOUD_MODELS: dict[str, ModelConfig] = {
    "claude-sonnet": ModelConfig(
        model_id="claude-sonnet-4-6",
        provider="anthropic",
        api_key_env="ANTHROPIC_API_KEY",
        max_tokens=8192,
    ),
    "claude-opus": ModelConfig(
        model_id="claude-opus-4-6",
        provider="anthropic",
        api_key_env="ANTHROPIC_API_KEY",
        max_tokens=8192,
    ),
    "gemini-pro": ModelConfig(
        model_id="gemini-2.5-pro",
        provider="google",
        api_key_env="GOOGLE_API_KEY",
        max_tokens=8192,
    ),
    "groq-llama": ModelConfig(
        model_id="llama-3.3-70b-versatile",
        provider="groq",
        api_key_env="GROQ_API_KEY",
        max_tokens=4096,
    ),
}

# ---------------------------------------------------------------------------
# Local Models (Ollama — runs on local hardware)
# ---------------------------------------------------------------------------
LOCAL_MODELS: dict[str, ModelConfig] = {
    "llama-70b": ModelConfig(
        model_id="llama3.3:70b",
        provider="ollama",
        base_url="http://localhost:11434",
        max_tokens=4096,
    ),
    "deepseek-r1": ModelConfig(
        model_id="deepseek-r1:70b",
        provider="ollama",
        base_url="http://localhost:11434",
        max_tokens=4096,
    ),
    "command-r-plus": ModelConfig(
        model_id="command-r-plus:104b",
        provider="ollama",
        base_url="http://localhost:11434",
        max_tokens=4096,
    ),
    "llama-8b": ModelConfig(
        model_id="llama3.1:8b",
        provider="ollama",
        base_url="http://localhost:11434",
        max_tokens=2048,
        temperature=0.3,
    ),
}

ALL_MODELS = {**CLOUD_MODELS, **LOCAL_MODELS}

# ---------------------------------------------------------------------------
# Agent Definitions (the four agents from the architecture)
# ---------------------------------------------------------------------------
AGENTS: dict[str, AgentConfig] = {
    "arthur": AgentConfig(
        name="Arthur",
        role="Chief of Staff",
        description="Coordinates tasks across all agents, manages priorities, and ensures alignment.",
        preferred_model="claude-opus",
        system_prompt=(
            "You are Arthur, Chief of Staff. You coordinate work across the team, "
            "prioritize tasks, delegate to the right agent, and ensure everything "
            "stays on track. You have final say on task assignment and scheduling."
        ),
    ),
    "ariadne": AgentConfig(
        name="Ariadne",
        role="CTO",
        description="Handles all technical decisions, code reviews, architecture, and engineering tasks.",
        preferred_model="claude-opus",
        system_prompt=(
            "You are Ariadne, CTO. You handle all technical decisions including "
            "architecture design, code review, debugging, infrastructure, and "
            "engineering best practices. You write and review code."
        ),
    ),
    "eames": AgentConfig(
        name="Eames",
        role="CMO",
        description="Manages marketing, content creation, copywriting, and brand strategy.",
        preferred_model="claude-sonnet",
        system_prompt=(
            "You are Eames, CMO. You handle marketing strategy, content creation, "
            "copywriting, social media, brand voice, and all customer-facing "
            "communications. You are creative and persuasive."
        ),
    ),
    "yusuf": AgentConfig(
        name="Yusuf",
        role="COO",
        description="Handles operations, process optimization, data analysis, and business logistics.",
        preferred_model="claude-sonnet",
        system_prompt=(
            "You are Yusuf, COO. You handle operations, process optimization, "
            "data analysis, reporting, logistics, and business efficiency. "
            "You are analytical and detail-oriented."
        ),
    ),
}

# ---------------------------------------------------------------------------
# Storage
# ---------------------------------------------------------------------------
MEMORY_DIR = os.environ.get("CLAUDE_AGENTS_MEMORY_DIR", "./data/memory")
LOGS_DIR = os.environ.get("CLAUDE_AGENTS_LOGS_DIR", "./data/logs")

# ---------------------------------------------------------------------------
# Watchdog
# ---------------------------------------------------------------------------
WATCHDOG_CHECK_INTERVAL = 30  # seconds
WATCHDOG_MODEL = "llama-8b"  # lightweight model for health checks
