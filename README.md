# Langgraph Agents Workflow

A modular, agent-based workflow built with [LangGraph].  
This repository demonstrates how to orchestrate multiple AI agents (e.g. market-price and government-scheme assistants) inside a single **StateGraph** and expose the graph as an API that can be served locally or inside Docker.

> **TL;DR** – If you just want to run it in Docker:
>
> ```bash
> docker build -t langgraph_agents .
> docker run -p 8000:8000 --env-file .env langgraph_agents
> ```

---

## Table of Contents
1. [Project layout](#project-layout)
2. [Quick start (local)](#quick-start-local)
3. [Environment variables](#environment-variables)
4. [Running with Docker](#running-with-docker)
5. [Adding new agents](#adding-new-agents)
6. [Useful Make targets](#useful-make-targets)

---

## Project layout
```
Langgraph_Agents/
├── agents/                 # Individual agent packages (each contains its own graph)
│   ├── market_price_agent/
│   └── gov_scheme_agent/
├── MCP/                    # Custom Model-Context-Protocol extensions
├── prompts/                # Prompt templates shared across agents
├── states/                 # Typed pydantic state definitions
├── storage/                # Persistence helpers (e.g. MongoDB checkpoints)
├── tools/                  # Custom LangChain / LangGraph tools
├── utils/                  # Misc utilities used by agents or main graph
├── main.py                 # Entrypoint – builds & compiles the top-level graph
├── Dockerfile              # Production container image
├── requirements.txt        # Python dependencies (locked versions)
└── .env                    # **Never commit secrets** – locally-scoped environment vars
```

### How it works
* `main.py` constructs a `StateGraph` composed of three nodes:
  * `agent_router` – async function that decides which specialised agent should handle the next step
  * `market_price_agent` – sub-graph that answers commodity-price queries
  * `gov_scheme_agent` – sub-graph that provides information on governmental schemes
* A `MongoDBSaver` checkpoint is configured so that graph state is persisted in MongoDB (connection string supplied via environment variable).
* When packaged with `langserve` (base image `langchain/langgraph-api`), the graph is served as a REST/gRPC API under `/agent`.

---

## Quick start (local)
1. **Clone and install dependencies**
   ```bash
   git clone <repo_url>
   cd Langgraph_Agents
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Set environment variables** – copy `.env.example` to `.env` (or create manually) and fill in values:
   ```bash
   # .env
   MONGO_CONNECTION_URL=mongodb://localhost:27017/langgraph
   # add any LLM API keys (OPENAI_API_KEY, GROQ_API_KEY, etc.)
   ```
3. **Run**
   ```bash
   python main.py
   # or if exposed via FastAPI / Uvicorn
   uvicorn main:app --reload
   ```

---

## Environment variables
| Variable                | Required | Description                                                 |
|-------------------------|----------|-------------------------------------------------------------|
| `MONGO_CONNECTION_URL`  | Yes      | Mongo connection string used by LangGraph checkpoint saver  |
| `OPENAI_API_KEY`        | Optional | If using OpenAI models inside any agent                     |
| `ANTHROPIC_API_KEY`     | Optional | If using Anthropic models                                   |
| `ANY_OTHER_API_KEY`     | Optional | Keys required by custom tools / agents                      |

Values are normally loaded automatically thanks to `python-dotenv` in `main.py`.

---

## Running with Docker
The `Dockerfile` is already optimised for minimal size and security (it removes `pip`, `setuptools`, and `wheel` in the final stage).

### Build image
```bash
docker build -t langgraph_agents .
```

### Run container
```bash
docker run -p 8000:8000 --env-file .env langgraph_agents
```

By default the base image (`langchain/langgraph-api:3.11`) will expose the graphs declared in `ENV LANGSERVE_GRAPHS` as REST endpoints. After the container is up, visit:
```
http://localhost:8000/agent/invoke
```
Or explore the interactive docs at:
```
http://localhost:8000/docs
```

---

## Adding new agents
1. Create a folder under `agents/` (e.g. `my_new_agent`).
2. Inside, implement a `graph.py` that defines `my_new_agent_graph`.
3. Update routing logic in `main.py` (`agent_router`) to recognise when to call the new agent.
4. Update `LANGSERVE_GRAPHS` (if you want separate endpoints) or just return the new sub-graph from the router.

---

## Useful Make targets
If you use **make**, you can add conveniences such as:
```Makefile
install:  ## Install deps in venv
	python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

serve:  ## Start local uvicorn server
	uvicorn main:app --reload --port 8000

docker-build:
	docker build -t langgraph_agents .

docker-run:
	docker run -p 8000:8000 --env-file .env langgraph_agents
```

*(Makefile is optional; commands above can be run manually)*

---

## License
This project is licensed under the MIT License – see `LICENSE` for details.
