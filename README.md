# ClinicalOps Agent

ClinicalOps Agent is a work-in-progress ADK project for clinical operations workflows.
It routes user requests to specialist agents and uses MongoDB MCP to read data from MongoDB Atlas.

## Current Status

This project is still in the development phase.
The main app loads, the MongoDB MCP smoke test works, and the agent structure is in place.
Some parts are still experimental and may change as development continues.

## What The Project Does

- Routes clinical questions to the right specialist agent.
- Screens patients for trial eligibility.
- Triage adverse events and side effects.
- Drafts regulatory documents and summaries.
- Uses MongoDB MCP as the bridge to MongoDB Atlas.

## Project Structure

- `app.py` - main ADK app and orchestrator.
- `agents/` - specialist agents and the ADK entrypoint.
- `agents/agent.py` - loader entrypoint for `adk web`.
- `test_mcp.py` - smoke test for the ADK + MongoDB MCP path.
- `Understand_this.md` - kid-friendly explanation of how the project works.
- `.env` - local environment settings such as `MONGODB_URI`.

## Setup

1. Create and activate the virtual environment if needed.
2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Make sure `.env` contains a valid MongoDB Atlas connection string.
4. Confirm the database name matches your MongoDB setup.

## Run The App

Use the local ADK executable from the virtual environment:

```powershell
.\.venv\Scripts\adk.exe web .
```

If your shell already knows `adk`, you can also try:

```powershell
adk web .
```

## Run The Smoke Test

This checks that the app loads and the MongoDB MCP path works:

```powershell
python test_mcp.py
```

## Development Notes

- The code is wired for ADK v2-style loading.
- `agents/agent.py` exists so `adk web` can discover `root_agent`.
- The app currently uses MCP over stdio with `mongodb-mcp-server`.
- The current focus is development and verification, not production hardening.

## Known Things To Watch

- Atlas network access must allow your machine.
- The MongoDB URI must be valid and point to the correct database.
- The web command may need the workspace-local ADK executable.

## Next Steps

- Tighten agent prompts and routing.
- Add more realistic tests.
- Add sample data or better fixtures for local development.
- Move toward a cleaner production-ready launch path once the behavior is stable.
