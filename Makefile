.PHONY: dev migrate seed test

# Run the backend and frontend locally without Docker.  The backend runs on
# port 8000 and the frontend on port 3000.  Ensure Postgres and Redis are
# available (e.g. via Docker Compose) or adjust ``DATABASE_URL`` accordingly.
dev:
	@echo "Starting backend..."
	uvicorn backend.app.main:app --reload &
	@echo "Starting frontend..."
	npm --prefix frontend run dev

# Apply database migrations using Alembic
migrate:
	cd backend && alembic upgrade head

# Seed the database with demo data
seed:
	python seed_data.py

# Run the test suite using pytest
test:
	pytest -q
