## Proof (Swagger screenshots)

### Database + CRUD
- CRUD + cleanup:
  - proof/database-migrations/swagger-get-notes-cleanup.png
  - proof/database-migrations/swagger-post-note-ok-cleanup.png
  - proof/database-migrations/swagger-put-note-ok-cleanup.png

- GET /notes/{id} returns 404 when missing:
  - proof/database-migrations/swagger-get-note-404-not-found.png

### Pagination
- Pagination:
  - proof/database-migrations/swagger-get-notes-pagination.png
  - proof/database-migrations/swagger-get-notes-pagination-offset-4.png

## Observability proof (request_id + safe errors)

- Request ID header on responses (/health):
  - proof/observability/swagger-health-200-request-id.png

- Standard 500 error response includes request_id:
  - proof/observability/swagger-500-standard-error-shape.png
  - proof/observability/swagger-500-error-with-request-id.png

- Verified test endpoint removed (/boom returns 404):
  - proof/observability/swagger-boom-404-after-delete.png

- Pagination validation (limit bounds):
  - proof/observability/swagger-get-notes-limit-validation.png

- 500 test seen + query restored (back to 200):
  - proof/observability/swagger-get-notes-restored-200.png

- GET /notes/{id} 404 includes request_id:
  - proof/observability/swagger-get-note-404-request-id.png
