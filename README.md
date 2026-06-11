# ClinicalOps Agent

An **AI-powered clinical operations assistant** built on Google's [ADK (Agent Development Kit)](https://cloud.google.com/agent-development-kit). It routes clinical questions — patient eligibility screening, adverse event triage, and regulatory document drafting — to specialist AI agents that query a MongoDB Atlas database via the [Model Context Protocol (MCP)](https://modelcontextprotocol.io).

## Table of Contents

- [Architecture](#architecture)
- [Agents](#agents)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Run the App](#run-the-app)
- [Tests](#tests)
- [Project Structure](#project-structure)
- [Security](#security)
- [Roadmap](#roadmap)

## Architecture

```
User (Streamlit UI or ADK CLI)
        │
        ▼
    ADK App  ──►  orchestrator_agent
                        │
            ┌───────────┼───────────┐
            ▼           ▼           ▼
    eligibility    ae_triage    regulatory_draft
    _screener      _agent       _agent
            │           │           │
            └───────────┼───────────┘
                        ▼
              MCPToolset (stdio)
                        │
                        ▼
            mongodb-mcp-server (npx)
                        │
                        ▼
              MongoDB Atlas (clinicalops)
```

The orchestrator receives a user request, routes it to the appropriate specialist agent, which uses MCP to read/write clinical data in MongoDB.

## Agents

| Agent | File | Responsibility |
|---|---|---|
| **Orchestrator** | `agents/orchestrator.py` | Routes requests to specialist agents; chains multi-step workflows |
| **Eligibility Screener** | `agents/eligibility_screener.py` | Matches patients against trial inclusion/exclusion criteria using semantic embeddings |
| **AE Triage** | `agents/ae_triage.py` | Grades adverse events against CTCAE v5; determines SAE status & regulatory reporting timelines |
| **Regulatory Draft** | `agents/regulatory_draft.py` | Generates ICH E2A-compliant SAE narratives and informed consent summaries |
| **MongoDB Agent** | `agents/mongodb_agent.py` | Generic agent for direct MongoDB queries (testing/utility) |

## Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3.11+** | Primary language |
| **Google ADK v2.1** | AI agent framework |
| **Gemini 2.5 Flash (Vertex AI)** | LLM backend |
| **text-embedding-004** | Semantic embeddings for patient-trial matching |
| **MCP v1.27** | Model Context Protocol — standard bridge between agents and tools |
| **mongodb-mcp-server** | MCP server exposing MongoDB operations as tools |
| **MongoDB Atlas** | Cloud document database (collections: `patients`, `trials`, `adverse_events`) |
| **Streamlit** | Web dashboard UI |
| **Firebase Auth** | Authentication (JWT token verification) |
| **Docker** | Production containerization |

## Prerequisites

- Python 3.11+
- Node.js 22+ (for `npx` to run `mongodb-mcp-server`)
- A [MongoDB Atlas](https://www.mongodb.com/atlas) cluster (free tier works)
- A [Google Cloud Project](https://console.cloud.google.com/) with Vertex AI and Application Default Credentials configured
- _(Optional)_ A Firebase project for production authentication

## Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/omi1811/clinicalOps-Agent.git
   cd clinicalOps-Agent
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/Mac
   .venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Copy the following into `.env`:
   ```env
   MONGODB_DB_NAME=clinicalops
   MONGODB_URI=mongodb+srv://<user>:<password>@<cluster>.mongodb.net/
   GOOGLE_CLOUD_PROJECT=clinicalops-agent
   GOOGLE_GENAI_USE_VERTEXAI=True
   FIREBASE_SERVICE_ACCOUNT_PATH=/etc/secrets/firebase/firebase_key.json
   ADK_LOG_LEVEL=INFO
   ```

5. **Authenticate with Google Cloud**
   ```bash
   gcloud auth application-default login
   ```

6. **Seed the database** (populates sample patients, trials, and adverse events)
   ```bash
   python seed_db.py
   ```

7. **Generate embeddings** (for semantic trial matching)
   ```bash
   python data/generate_embeddings.py
   ```

8. **Verify the setup**
   ```bash
   python setup_test.py
   ```

## Run the App

### Streamlit Dashboard (recommended)
```bash
streamlit run frontend/app.py
```
Opens a 3-tab UI: **Eligibility Screening**, **Adverse Event Triage**, and **Regulatory Draft**.

### ADK CLI (developer mode)
```bash
adk web .
```
ADK automatically discovers `agents/agent.py` and serves an interactive web interface.

### Docker
```bash
docker build -t clinicalops-agent .
docker run -p 8080:8080 clinicalops-agent
```

## Tests

| Command | What it checks |
|---|---|
| `python setup_test.py` | Environment variables, MongoDB connectivity, Gemini API client |
| `python test_mcp.py` | Full ADK + MongoDB MCP integration (lists collections, queries patients) |
| `python mcp_test.py` | MCP toolset instantiation |
| `python test_mcp_tools.py` | Lists all available MCP tools |
| `python mongo_test.py` | Direct MongoDB ping |
| `python test_auth.py` | Firebase auth layer (mock + real token) |

## Project Structure

```
├── agents/                    # ADK specialist agents
│   ├── agent.py               # ADK web entrypoint (exports root_agent)
│   ├── orchestrator.py        # Central routing agent
│   ├── eligibility_screener.py # Patient-trial eligibility matching
│   ├── ae_triage.py           # Adverse event CTCAE grading
│   ├── regulatory_draft.py    # ICH-compliant document drafting
│   ├── mongodb_agent.py       # Generic MongoDB query agent
│   ├── mcp_config.py          # MCP toolset factory
│   └── shared_mcp.py          # Singleton shared MCP toolset instance
├── auth/                      # Firebase authentication
│   └── firebase_auth.py       # Auth manager (prod + mock modes)
├── data/
│   └── generate_embeddings.py # Vertex AI embedding generation
├── frontend/
│   └── app.py                 # Streamlit dashboard
├── mcp/
│   └── mongodb-mcp-config.json # MCP server configuration
├── services/
│   └── adk_runner.py          # ADK runner with persistent event loop
├── utils/
│   └── logger.py              # Centralized logging
├── app.py                     # Main ADK application definition
├── db.py                      # Direct PyMongo helpers (utility scripts)
├── seed_db.py                 # Sample data seeder
├── Dockerfile                 # Production build
├── requirements.txt           # Python dependencies
└── .env                       # Environment configuration
```

## Security

- **Read-only vs read-write**: The eligibility screener uses a read-only MCP connection. Only AE triage and regulatory drafting use read-write access.
- **DDL operations blocked**: Dangerous operations (`drop-collection`, `drop-database`, `create-index`, `rename-collection`) are disabled via `MDB_MCP_DISABLED_TOOLS`.
- **Query limits**: `max_documents_per_query: 5`, `max_bytes_per_query: 200000`.
- **Authentication**: Firebase Auth with JWT verification in production; mock mode for local development.
- **No direct API keys**: Uses Vertex AI with Application Default Credentials — no Gemini API key required.

## Roadmap

- [x] Core agent structure and routing
- [x] MongoDB MCP integration
- [x] Patient-trial eligibility matching with embeddings
- [x] CTCAE adverse event triage
- [x] ICH E2A regulatory document drafting
- [x] Streamlit dashboard UI
- [x] Firebase authentication
- [x] Docker deployment
- [ ] Production hardening and error handling
- [ ] Comprehensive test suite
- [ ] CI/CD pipeline
- [ ] Multi-language support
