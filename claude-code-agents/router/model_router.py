"""
Model Router — replaces LiteLLM as the receptionist & task manager.

Routes requests to the right model based on task type, agent preference,
and model availability. Supports both cloud and local (Ollama) models.
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
from dataclasses import dataclass, field
from enum import Enum

import anthropic
import httpx

from config import ALL_MODELS, ModelConfig

logger = logging.getLogger(__name__)


class TaskComplexity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class RoutingDecision:
    model_id: str
    provider: str
    reason: str


@dataclass
class ModelStatus:
    model_id: str
    available: bool = True
    last_check: float = 0.0
    avg_latency_ms: float = 0.0
    error_count: int = 0


class ModelRouter:
    """
    Routes tasks to the optimal model based on:
    - Agent preference
    - Task complexity
    - Model availability
    - Latency requirements
    """

    def __init__(self) -> None:
        self.models = ALL_MODELS
        self.status: dict[str, ModelStatus] = {
            key: ModelStatus(model_id=cfg.model_id)
            for key, cfg in self.models.items()
        }
        self._anthropic_client: anthropic.AsyncAnthropic | None = None
        self._http_client: httpx.AsyncClient | None = None

    async def start(self) -> None:
        self._anthropic_client = anthropic.AsyncAnthropic()
        self._http_client = httpx.AsyncClient(timeout=30.0)
        logger.info("ModelRouter started — %d models registered", len(self.models))

    async def stop(self) -> None:
        if self._http_client:
            await self._http_client.aclose()
        if self._anthropic_client:
            await self._anthropic_client.close()

    def route(
        self,
        preferred_model: str,
        complexity: TaskComplexity = TaskComplexity.MEDIUM,
    ) -> RoutingDecision:
        """Pick the best available model for a request."""
        # Try preferred model first
        if preferred_model in self.models and self._is_available(preferred_model):
            cfg = self.models[preferred_model]
            return RoutingDecision(
                model_id=cfg.model_id,
                provider=cfg.provider,
                reason=f"Using preferred model: {preferred_model}",
            )

        # Fallback chain based on complexity
        fallback_chain = self._get_fallback_chain(complexity)
        for model_key in fallback_chain:
            if model_key in self.models and self._is_available(model_key):
                cfg = self.models[model_key]
                return RoutingDecision(
                    model_id=cfg.model_id,
                    provider=cfg.provider,
                    reason=f"Fallback from {preferred_model} to {model_key}",
                )

        # Last resort: any available model
        for key, status in self.status.items():
            if status.available:
                cfg = self.models[key]
                return RoutingDecision(
                    model_id=cfg.model_id,
                    provider=cfg.provider,
                    reason=f"Last resort: {key}",
                )

        raise RuntimeError("No models available")

    async def send(
        self,
        model_key: str,
        messages: list[dict],
        system: str = "",
        max_tokens: int | None = None,
    ) -> str:
        """Send a message to a model and return the response text."""
        cfg = self.models[model_key]
        max_tokens = max_tokens or cfg.max_tokens

        start = time.monotonic()
        try:
            if cfg.provider == "anthropic":
                text = await self._send_anthropic(cfg, messages, system, max_tokens)
            elif cfg.provider == "ollama":
                text = await self._send_ollama(cfg, messages, system, max_tokens)
            elif cfg.provider in ("google", "groq"):
                text = await self._send_openai_compat(cfg, messages, system, max_tokens)
            else:
                raise ValueError(f"Unknown provider: {cfg.provider}")

            elapsed = (time.monotonic() - start) * 1000
            self._record_success(model_key, elapsed)
            return text

        except Exception as e:
            self._record_failure(model_key)
            raise

    # ------------------------------------------------------------------
    # Provider-specific send methods
    # ------------------------------------------------------------------

    async def _send_anthropic(
        self, cfg: ModelConfig, messages: list[dict], system: str, max_tokens: int
    ) -> str:
        assert self._anthropic_client is not None
        kwargs: dict = {
            "model": cfg.model_id,
            "max_tokens": max_tokens,
            "messages": messages,
        }
        if system:
            kwargs["system"] = system
        resp = await self._anthropic_client.messages.create(**kwargs)
        return resp.content[0].text

    async def _send_ollama(
        self, cfg: ModelConfig, messages: list[dict], system: str, max_tokens: int
    ) -> str:
        assert self._http_client is not None
        payload: dict = {
            "model": cfg.model_id,
            "messages": messages,
            "stream": False,
            "options": {"num_predict": max_tokens, "temperature": cfg.temperature},
        }
        if system:
            payload["messages"] = [{"role": "system", "content": system}] + messages

        resp = await self._http_client.post(
            f"{cfg.base_url}/api/chat", json=payload
        )
        resp.raise_for_status()
        return resp.json()["message"]["content"]

    async def _send_openai_compat(
        self, cfg: ModelConfig, messages: list[dict], system: str, max_tokens: int
    ) -> str:
        """Send via OpenAI-compatible API (Groq, Google AI Studio, etc.)."""
        assert self._http_client is not None
        base = cfg.base_url or self._default_base_url(cfg.provider)
        all_messages = messages
        if system:
            all_messages = [{"role": "system", "content": system}] + messages

        resp = await self._http_client.post(
            f"{base}/v1/chat/completions",
            headers={"Authorization": f"Bearer {cfg.api_key}"},
            json={
                "model": cfg.model_id,
                "messages": all_messages,
                "max_tokens": max_tokens,
                "temperature": cfg.temperature,
            },
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]

    # ------------------------------------------------------------------
    # Health & status helpers
    # ------------------------------------------------------------------

    async def health_check(self, model_key: str) -> bool:
        """Ping a model to see if it's reachable."""
        cfg = self.models.get(model_key)
        if not cfg:
            return False
        try:
            if cfg.provider == "ollama":
                assert self._http_client is not None
                resp = await self._http_client.get(f"{cfg.base_url}/api/tags")
                return resp.status_code == 200
            # For cloud models, assume available if API key is set
            return bool(cfg.api_key)
        except Exception:
            return False

    async def check_all(self) -> dict[str, bool]:
        results = {}
        for key in self.models:
            results[key] = await self.health_check(key)
            self.status[key].available = results[key]
            self.status[key].last_check = time.time()
        return results

    def _is_available(self, key: str) -> bool:
        return self.status.get(key, ModelStatus(model_id="")).available

    def _record_success(self, key: str, latency_ms: float) -> None:
        s = self.status[key]
        s.avg_latency_ms = (s.avg_latency_ms * 0.8) + (latency_ms * 0.2)
        s.error_count = max(0, s.error_count - 1)
        s.available = True

    def _record_failure(self, key: str) -> None:
        s = self.status[key]
        s.error_count += 1
        if s.error_count >= 3:
            s.available = False
            logger.warning("Model %s marked unavailable after %d errors", key, s.error_count)

    def _get_fallback_chain(self, complexity: TaskComplexity) -> list[str]:
        if complexity == TaskComplexity.CRITICAL:
            return ["claude-opus", "claude-sonnet", "gemini-pro", "llama-70b"]
        if complexity == TaskComplexity.HIGH:
            return ["claude-sonnet", "claude-opus", "llama-70b", "deepseek-r1"]
        if complexity == TaskComplexity.MEDIUM:
            return ["claude-sonnet", "groq-llama", "llama-70b", "command-r-plus"]
        return ["groq-llama", "llama-8b", "llama-70b"]

    @staticmethod
    def _default_base_url(provider: str) -> str:
        return {
            "groq": "https://api.groq.com/openai",
            "google": "https://generativelanguage.googleapis.com",
        }.get(provider, "")
