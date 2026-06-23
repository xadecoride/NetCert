.PHONY: dev-backend dev-frontend dev-infra build-backend build-frontend build-all test-backend migrate-up migrate-down up down clean

# Development
dev-infra:
	docker compose -f infra/docker-compose.yml up -d postgres redis

dev-backend:
	cd backend && go run ./cmd/server/

dev-frontend:
	cd frontend && npm run dev

dev-all: dev-infra
	@echo "Starting backend and frontend..."
	@cd backend && go run ./cmd/server/ &
	@cd frontend && npm run dev

# Full stack via Docker Compose
up:
	docker compose -f infra/docker-compose.yml up --build -d

down:
	docker compose -f infra/docker-compose.yml down

# Build
build-backend:
	cd backend && go build -o bin/server ./cmd/server/

build-frontend:
	cd frontend && npm run build

build-all: build-backend build-frontend

# Database
migrate-up:
	psql -U netcert -d netcert -f backend/migrations/001_initial_schema.sql
	psql -U netcert -d netcert -f backend/migrations/002_seed_data.sql

migrate-down:
	psql -U netcert -d netcert -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

# Testing
test-backend:
	cd backend && go test ./...

# Other
clean:
	rm -rf backend/bin frontend/.next frontend/node_modules
