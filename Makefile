# Файл: Makefile

.PHONY: help build up down restart logs shell status clean

help:
	@echo "🔧 Aevi Commands:"
	@echo "  make build    - Build all Docker images"
	@echo "  make up       - Start all services"
	@echo "  make down     - Stop all services"
	@echo "  make restart  - Restart all services"
	@echo "  make logs     - Show logs"
	@echo "  make shell    - Enter backend shell"
	@echo "  make status   - Show service status"
	@echo "  make clean    - Remove all containers and volumes"
	@echo "  make seed     - Run database seeding"

build:
	docker-compose build --no-cache

up:
	docker-compose up -d
	@echo "✅ Aevi is running!"
	@echo "📍 Frontend: http://localhost"
	@echo "📍 API docs: http://localhost:8000/api/docs"
	@echo "📍 PgAdmin: http://localhost:5050 (dev only)"

down:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f --tail=100

shell:
	docker-compose exec backend bash

status:
	docker-compose ps

clean:
	docker-compose down -v
	docker system prune -f

seed:
	docker-compose exec backend python -m app.database.seed_data

migrate:
	docker-compose run --rm migrations

dev:
	docker-compose --profile dev up -d
	@echo "🛠️ Development mode with PgAdmin enabled"