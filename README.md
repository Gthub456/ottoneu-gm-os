# Ottoneu GM Operating System

Welcome to the **Ottoneu GM Operating System**&mdash;a unified toolkit for the serious fantasy baseball general manager.  This project combines a FastAPI backend, a Next.js frontend, scheduled data ingesters and a Postgres/Redis data stack into one deployable unit.  Use this app to view your Ottoneu roster, analyze players, evaluate trades, track news and projections, and receive automated recommendations without manually entering any data.

## Overview

This repository is organised into two main applications:

| Folder      | Description                                        |
|------------:|:----------------------------------------------------|
| **backend** | A FastAPI service exposing REST endpoints, a SQLAlchemy data model, Celery tasks for ingesting data, and connectors for pulling data from Ottoneu and other public sources.  Database migrations live in `backend/alembic`. |
| **frontend** | A Next.js + TypeScript single‑page app styled with Tailwind CSS.  It connects to the backend to display roster tables, free agent lists, market analytics, trade evaluations and more. |

Docker Compose bundles Postgres, Redis, the API service, the Celery worker and the Next.js app so you can start everything with a single command.

## Getting Started

### Prerequisites

* [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed on your machine.

### Local Development

1. Clone this repository:

   ```bash
   git clone https://example.com/yourusername/ottoneu-gm-os.git
   cd ottoneu-gm-os
   ```

2. Copy the sample environment file and fill in any secrets.  At a minimum you must set `OTTONEU_LEAGUE_ID` to your league ID (for demo mode you can leave it blank):

   ```bash
   cp .env.example .env
   # edit .env to set secrets
   ```

3. Build and start the entire stack using Docker Compose:

   ```bash
   docker compose up --build
   ```

   The first run may take a few minutes.  This command starts:

   * `backend`: FastAPI server on [http://localhost:8000](http://localhost:8000)
   * `worker`: Celery worker executing periodic ingestion tasks
   * `frontend`: Next.js app on [http://localhost:3000](http://localhost:3000)
   * `db`: Postgres database
   * `redis`: Redis cache/queue

4. Visit the frontend at <http://localhost:3000>.  When no Ottoneu connection exists the app runs in **demo mode** with seeded sample data.  Use the **Connect Ottoneu** button to sign in and sync your real team.

### Make Commands

The provided `Makefile` includes a few convenience shortcuts:

```bash
make dev        # run backend and frontend locally without Docker
make migrate    # run database migrations
make seed       # seed demo data into the database
make test       # run the pytest test suite
```

## Architecture

The platform is composed of the following services:

* **FastAPI backend** (`backend/app/main.py`)
  * Exposes REST APIs under `/api` for roster data, free agents, trades, and more.
  * Uses SQLAlchemy models defined in `backend/app/models.py` with Alembic migrations.
  * Implements connectors in `backend/app/connectors` for Ottoneu scraping, Statcast ingestion, projections and news.  Connectors are run asynchronously via Celery tasks.
  * Provides authentication and a secure OAuth‑like flow for capturing Ottoneu cookies.

* **Celery worker** (`backend/app/tasks.py`)
  * Periodically invokes connectors to update the database.
  * Uses Redis as a broker and result backend.

* **Next.js frontend** (`frontend/`)
  * Uses React, TypeScript, Tailwind CSS and TanStack Table.
  * Fetches roster data and recommendations from the backend and displays them in interactive tables and charts.
  * Pages include Home (GM Terminal), Roster, Free Agents, Trade Machine, Market, Player Lab and Data Health.

* **PostgreSQL** database
* **Redis** for caching and queuing

## Demo Mode

Before you connect your Ottoneu account the app runs in *demo mode*, loading sample players and rosters from the seeds provided in `seed_data.py`.  This lets you explore the UI immediately.  Once you click **Connect Ottoneu** and complete the login flow the ingestion workers will synchronise your real team automatically.

## Contributing

This project is intended as a starting point; it is not complete.  Areas you may wish to extend include:

* Hardening the Ottoneu scraping connector with Playwright and robust DOM selectors.
* Implementing additional analytics (Statcast, projections, replacement levels).
* Improving the decision engines for trade evaluation and lineup optimisation.
* Adding tests for each connector and engine.

## License

This project is provided as-is for educational purposes.
