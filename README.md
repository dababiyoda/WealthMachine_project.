# WealthMachine_project

A system that continuously identifies, validates and scales digital business opportunities using AI agents and a knowledge graph. Success is measured by compounding returns and resiliency *(P(failure) ≤ 0.01%)*.

## Deploying on Replit

1. Fork this repository and create a new Replit project from it.
2. Open the Replit shell and install the dependencies:
   ```bash
   pip install -e .
   ```
3. Add the required environment variables under the **Secrets** tab:
   - `NEO4J_URI` – connection URI to your Neo4j instance.
   - `NEO4J_USER` – Neo4j username.
   - `NEO4J_PASSWORD` – Neo4j password.
   - `DATABASE_URL` – Postgres connection string.
   - `CELERY_BROKER_URL` – Redis broker URL for Celery.
   - `CELERY_RESULT_BACKEND` – Celery result backend (usually the same Redis URL).

## Running the system

### Celery agents

Start the Celery worker to execute agents in the background:

```bash
celery -A src.celery_app worker --loglevel=info
```

### Prefect workflows

Prefect flows live in `src/workflows`. To run them:

```bash
prefect deploy src/workflows/workflow_engine.py:wealth_machine_flow -n wealth-machine
prefect agent start -q default
prefect run flow-name=wealth-machine
```

Make sure Prefect is connected to a Prefect server or Prefect Cloud as described in the Prefect documentation.
