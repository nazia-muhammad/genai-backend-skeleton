# GenAI Backend Skeleton (FastAPI)
Proof (Swagger after cleanup): proof/week-3/swagger-get-notes-cleanup.png | proof/week-3/swagger-post-note-ok-cleanup.png | proof/week-3/swagger-put-note-ok-cleanup.png
A simple FastAPI backend providing CRUD endpoints for notes (starter backend for future GenAI features).

## Run locally

1) Activate the conda environment:
```bash
conda activate ai
```
2) Start the server:
```bash
uvicorn main:app --reload
```
## API Docs (Swagger)

Once running, open:
- http://127.0.0.1:8000/docs
Note: This works only while the server is running locally.
