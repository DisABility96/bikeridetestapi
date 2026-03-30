# AI Usage Reflection

## 1. Which AI tool or tools did you use?
I used **DeepSeek** during the development of this project.

## 2. What prompts or instructions did you give?
- **Initial prompt**: “Build a Bike Ride Service API with FastAPI and SQLite. Endpoints: /ride/start, /ride/end, /ride/{id}, /ride/{id}/cost. Pricing: $5 unlock, first 15 min free, then $1 per 5 min, daily cap $25.”
- **Follow‑up prompts**:
  - “How to structure the project for readability?”
  - “Provide error handling examples.”
  - “Generate unit tests for the endpoints.”
  - “Explain how to handle idempotency and concurrency.”
  - “Help me fix the PermissionError when cleaning up test databases on Windows.”

## 3. What mistakes, weaknesses, or blind spots did the AI-generated output have?
- **Time handling**: AI initially used naive `datetime.utcnow()`, which is deprecated and not timezone‑aware. I replaced it with `datetime.now(timezone.utc)`.
- **Error response codes**: Some suggestions used `400 Bad Request` for already‑ended rides, but `409 Conflict` is more semantically correct.
- **SQL injection**: The generated SQL used string formatting in a few places; I verified that all queries use parameter placeholders (`?`).
- **Missing status check**: The `end_ride` function didn’t verify the ride wasn’t already ended; I added a status check to prevent double‑ending.
- **Test cleanup**: The initial test fixture tried to delete the database file immediately after the test, causing `PermissionError` on Windows because the connection was still open. I added garbage collection and a small delay, and wrapped the deletion in a `try/except`.

## 4. What did you manually verify, fix, or improve?
- **Cost calculation**: I manually tested edge cases (duration exactly 15 min, 18 min, 2 hours, 24 hours) to ensure the ceiling logic and daily cap worked correctly.
- **Error handling**: I verified that all endpoints return appropriate HTTP status codes and meaningful error messages.
- **Database schema**: I added a `status` column (`active`/`completed`) to simplify queries and improve clarity.
- **Code organization**: I separated concerns into `crud.py`, `utils.py`, `schemas.py`, and `routes/` for maintainability.
- **Unit tests**: I wrote comprehensive tests covering normal flows and error scenarios, and fixed the Windows cleanup issue.
- **Documentation**: I updated the README with clear setup instructions and example requests.
- **Concurrency**: I ensured that `end_ride` updates the database atomically within a transaction, which SQLite handles well.

Overall, AI accelerated development significantly, but careful review and manual adjustments were essential to ensure correctness, security, and adherence to best practices.