- ✅ **Reliability foundation**
  - ✅ Confirmed centralized error helpers in `app/errors.py` (400/401/403/404/409/500)
  - ✅ Added retry helper template in `app/utils/retry.py` (`retry_with_backoff`) for future external calls (LLM/HTTP)

- ✅ **Auth foundation**
  - ✅ Added password hashing helpers in `app/auth.py` (hash + verify)
  - ✅ Pinned deps: `passlib==1.7.4`, `bcrypt==3.2.2`
  - ✅ Verified hashing works (prints True)

