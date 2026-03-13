# neuro-san-gemini-example

A minimal reference implementation of a [Neuro-SAN](https://github.com/cognizant-ai-lab/neuro-san) agent network powered by **Google Gemini on Vertex AI**, authenticated via **Application Default Credentials (ADC)** — no API key required.

This example demonstrates how to wire a Neuro-SAN agent to a Vertex AI-hosted Gemini model using your organization's GCP identity, making it suitable for enterprise and on-prem-to-cloud deployments.

---

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [1. Google Cloud Authentication](#1-google-cloud-authentication)
- [2. Environment Setup](#2-environment-setup)
- [3. Python Environment Setup](#3-python-environment-setup)
- [4. Configuration](#4-configuration)
- [5. Running the Server](#5-running-the-server)
- [6. Verification](#6-verification)
- [Project Structure](#project-structure)
- [References](#references)

---

## Overview

| Component | Technology |
|---|---|
| Agent Framework | [Neuro-SAN](https://github.com/cognizant-ai-lab/neuro-san) |
| LLM Provider | Google Vertex AI (`ChatVertexAI`) |
| Model | `gemini-2.5-flash` (configurable) |
| Authentication | Application Default Credentials (ADC) |
| Config Format | HOCON |

The included agent (`greeter`) is a simple IT Support Greeter that welcomes users and captures the nature of their issue — it serves as a working scaffold for building more complex agent networks.

---

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.10+**
- **[Google Cloud CLI](https://cloud.google.com/sdk/docs/install)** (`gcloud`)
- Access to a GCP project with the **Vertex AI API** enabled

---

## 1. Google Cloud Authentication

Authenticate your local environment with GCP using Application Default Credentials:

```bash
gcloud auth login
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
```

> **Note:** Do **not** set a `GOOGLE_API_KEY` environment variable when using ADC. The two authentication paths are mutually exclusive — if `GOOGLE_API_KEY` is present, it may take precedence and cause unexpected errors.

---

## 2. Environment Setup

Copy the provided template and fill in your project details:

```bash
cp .env.example .env
```

Open `.env` and update the following variables:

```dotenv
GCP_PROJECT_ID=your-gcp-project-id
GCP_REGION=your-vertex-ai-region   # e.g. us-central1, europe-west4, asia-south1

AGENT_MANIFEST_FILE=registries/manifest.hocon
LOG_LEVEL=DEBUG
LANGCHAIN_VERBOSE=true
```

| Variable | Description |
|---|---|
| `GCP_PROJECT_ID` | Your target Google Cloud project ID |
| `GCP_REGION` | The Vertex AI region to use |
| `AGENT_MANIFEST_FILE` | Path to the agent network manifest |
| `LOG_LEVEL` | Logging verbosity (`DEBUG`, `INFO`, `WARNING`) |
| `LANGCHAIN_VERBOSE` | Enable LangChain verbose output (`true` / `false`) |

---

## 3. Python Environment Setup

### Standard Python (recommended)

Create and activate a virtual environment, then install dependencies:

```bash
# Create virtual environment
python -m venv venv

# Activate — Linux / macOS
source venv/bin/activate

# Activate — Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### Using uv

If you are using [uv](https://github.com/astral-sh/uv) as your package manager:

```bash
uv venv
uv pip install -r requirements.txt
```

---

## 4. Configuration

The configuration is intentionally split to keep LLM logic separate from agent definitions.

### `registries/llm_config.hocon`

Defines the Vertex AI LLM parameters. The `project` and `location` values are read from environment variables at runtime via HOCON substitution — no credentials are hardcoded.

```hocon
llm_config: {
    class: "langchain_google_vertexai.chat_models.ChatVertexAI"
    model_name: "gemini-2.5-flash"   # configurable: any Vertex AI Gemini model
    temperature: 0.2                 # 0.0 (deterministic) to 1.0 (creative)
    max_tokens: 2048                 # maximum tokens in the model's response
    project: ${GCP_PROJECT_ID}
    location: ${GCP_REGION}
}
```

### `registries/greeter.hocon`

Defines the agent network. It uses the `include` directive to inherit the shared LLM configuration:

```hocon
{
    include "registries/llm_config.hocon"

    tools: [
        {
            name: "greeter"
            ...
        }
    ]
}
```

> **Encoding Note:** Ensure all `.hocon` files are saved with **UTF-8 (without BOM)** encoding. Some editors default to UTF-8 with BOM, which can cause the HOCON parser to fail silently.

---

## 5. Running the Server

The `start_server.py` script loads environment variables from `.env` and starts the Neuro-SAN server:

```bash
python start_server.py
```

On a successful start, you should see output similar to:

```
1. Loading Environment Variables from .env...
2. Environment locked. Targeting GCP Project: your-project-id (us-central1)
3. Igniting Neuro SAN Server...
```

> If you are using uv: `uv run python start_server.py`

---

## 6. Verification

With the server running, open a **new terminal** and run the test client:

```bash
python test_client.py
```

The script sends a sample message to the `greeter` agent and streams the response to your terminal:

```
Connecting to Neuro SAN Greeter...

----------------------------------------
Hello! Welcome to IT Support. I'm here to help...
----------------------------------------
Stream complete!
```

> If you see `Error: Could not connect`, make sure the server (step 5) is still running in the other terminal.

---

## Project Structure

```
neuro-san-gemini-example/
├── coded_tools/            # Custom coded tools (Python)
├── registries/
│   ├── llm_config.hocon   # Shared Vertex AI LLM configuration
│   ├── greeter.hocon      # Greeter agent network definition
│   └── manifest.hocon     # Agent manifest (lists active networks)
├── .env.example           # Environment variable template
├── requirements.txt       # Python dependencies
├── start_server.py        # Server entry point
├── test_client.py         # Streaming test client
└── user_guide.md          # Detailed configuration reference
```

---

## References

- [Neuro-SAN](https://github.com/cognizant-ai-lab/neuro-san) — Agent framework
- [Neuro-SAN Studio](https://github.com/cognizant-ai-lab/neuro-san-studio) — Examples and templates
- [LangChain ChatVertexAI](https://python.langchain.com/docs/integrations/chat/google_vertex_ai_palm/) — LangChain Vertex AI integration
- [Vertex AI Authentication](https://cloud.google.com/vertex-ai/docs/authentication) — GCP ADC documentation
- [Application Default Credentials](https://cloud.google.com/docs/authentication/application-default-credentials) — Google ADC guide
