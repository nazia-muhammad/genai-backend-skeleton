# GenAI Backend Skeleton (FastAPI)

A simple FastAPI backend providing CRUD endpoints for notes (starter backend for future GenAI features).

## Proof (Swagger screenshots)

- CRUD + cleanup:
  - proof/database-migrations/swagger-get-notes-cleanup.png
  - proof/database-migrations/swagger-post-note-ok-cleanup.png
  - proof/database-migrations/swagger-put-note-ok-cleanup.png
  - proof/database-migrations/swagger-get-note-404-not-found.png

- Pagination:
  - proof/database-migrations/swagger-get-notes-pagination.png
  - proof/database-migrations/swagger-get-notes-pagination-offset-4.png

- Error handling test cleanup:
  - proof/database-migrations/swagger-boom-404-after-delete.png

proof/observability/swagger-get-note-404-request-id.png

## Run locally

1) Activate the conda environment:
```bash
conda activate ai
