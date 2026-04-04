# Claude Code Agents

Multi-agent AI system powered by **Claude Code** — a drop-in replacement for OpenClaw.

```
  ┌─────────────────────────────────────────────────────────┐
  │                  Communication Layer                     │
  │              Slack  ·  Telegram  ·  CLI                  │
  └──────────────────────────┬──────────────────────────────┘
                             │
  ┌──────────────────────────▼──────────────────────────────┐
  │                     Orchestrator                         │
  │         Receives messages · Routes · Stores results      │
  └──────────────────────────┬──────────────────────────────┘
                             │
  ┌──────────────────────────▼──────────────────────────────┐
  │                 Model Router (replaces LiteLLM)          │
  │   Routes tasks to optimal model based on complexity,     │
  │   agent preference, and availability                     │
  │                                                          │
  │   Cloud Models          │  Local Models (Ollama)         │
  │   ─────────────         │  ────────────────────          │
  │   Claude Opus 4.6       │  llama3.3:70b                  │
  │   Claude Sonnet 4.6     │  deepseek-r1:70b               │
  │   Gemini 2.5 Pro        │  command-r-plus:104b           │
  │   Groq llama-3.3-70b    │  llama3.1:8b (watchdog)        │
  └──────────────────────────┬──────────────────────────────┘
                             │
  ┌──────────────────────────▼──────────────────────────────┐
  │               AI Agents (work simultaneously)            │
  │                                                          │
  │   Arthur          Ariadne        Eames         Yusuf     │
  │   Chief of Staff  CTO            CMO           COO       │
  │   Coordinates &   Technical &    Marketing &   Operations│
  │   delegates       engineering    content       & data     │
  └──────────────────────────┬──────────────────────────────┘
                             │
  ┌──────────────────────────▼──────────────────────────────┐
  │                    Storage & Memory                      │
  │     Per-agent memory · Task logs · Persistent state      │
  └─────────────────────────────────────────────────────────┘
                             │
  ┌──────────────────────────▼──────────────────────────────┐
  │                       Watchdog                           │
  │     Health checks · Model availability · System monitor  │
  └─────────────────────────────────────────────────────────┘
```

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your API key
export ANTHROPIC_API_KEY="sk-ant-..."

# 3. Run in interactive CLI mode
python main.py --cli

# 4. Or ask a one-shot question
python main.py --ask "Design a REST API for a task manager"
```

## Communication Channels

| Channel   | Required Env Vars                           |
|-----------|---------------------------------------------|
| CLI       | None (built-in)                             |
| Slack     | `SLACK_BOT_TOKEN`, `SLACK_APP_TOKEN`        |
| Telegram  | `TELEGRAM_BOT_TOKEN`                        |

```bash
# Run as server with Slack + Telegram
export SLACK_BOT_TOKEN="xoxb-..."
export SLACK_APP_TOKEN="xapp-..."
export TELEGRAM_BOT_TOKEN="123456:ABC..."
python main.py
```

## Agents

| Agent    | Role            | Focus Area                              |
|----------|-----------------|----------------------------------------|
| Arthur   | Chief of Staff  | Task coordination, delegation, priority |
| Ariadne  | CTO             | Code, architecture, technical decisions |
| Eames    | CMO             | Content, marketing, brand, copywriting  |
| Yusuf    | COO             | Operations, data analysis, logistics    |

### Talking to a specific agent

```
You> @ariadne Review this Python function for security issues
You> @eames Write a product launch email
You> @yusuf Analyze our Q4 conversion data
```

## Optional: Local Models (Ollama)

For privacy-preserving local inference, install [Ollama](https://ollama.com) and pull models:

```bash
ollama pull llama3.3:70b
ollama pull deepseek-r1:70b
ollama pull command-r-plus:104b
ollama pull llama3.1:8b  # used by watchdog
```

## Optional: Additional Cloud Models

```bash
export GOOGLE_API_KEY="..."    # Gemini 2.5 Pro
export GROQ_API_KEY="..."      # Groq llama-3.3-70b
```

## Project Structure

```
claude-code-agents/
├── main.py               # Entry point (CLI, server, one-shot)
├── orchestrator.py        # Central brain — ties everything together
├── watchdog.py            # System health monitor
├── config.py              # All configuration (models, agents, storage)
├── requirements.txt
├── router/
│   └── model_router.py    # Routes tasks to optimal model
├── agents/
│   ├── base_agent.py      # Base agent with memory & task handling
│   └── team.py            # Agent team — simultaneous work
├── comms/
│   ├── slack_bot.py       # Slack Socket Mode integration
│   └── telegram_bot.py    # Telegram bot integration
└── storage/
    └── memory_store.py    # Persistent task logs & agent memory
```
