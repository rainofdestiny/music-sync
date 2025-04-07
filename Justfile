default: 
  docker-compose up --build -d 

ruff: 
  uv run ruff check .

black: 
  uv run black .

dev: black ruff 
  docker-compose up --build 
