app:
  uvicorn app.main:app --host 0.0.0.0 --port 8000

dev:
  uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

shell:
  source $(poetry env info --path)/bin/activate

