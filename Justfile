default:
  docker-compose up --build -d

lint:
    uv run ruff check . --fix
    uv run black .

dev: # black ruff
  docker-compose up --build

app:
    docker exec -it app bash

psql:
    docker exec -it postgres psql -U postgres

mm *args:
  uv run alembic revision --autogenerate -m "{{args}}"

migrate:
  uv run alembic upgrade head
