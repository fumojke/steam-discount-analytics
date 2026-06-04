# Steam Discount Analytics API

A modern backend service built with FastAPI to track Steam wishlist game prices, analyze discounts, and automatically update data via background tasks.

## Tech Stack
- **Framework:** FastAPI
- **Package Manager:** uv (Astral)
- **ORM:** SQLAlchemy
- **Database:** SQLite
- **Scheduler:** APScheduler

## Features
- Automatically syncs and updates game prices every 12 hours using background workers.
- Full CRUD functionality for managing tracked games.
- Data validation and serialization via Pydantic schemas.
- Interactive API documentation powered by Swagger UI.

## Getting Started

### Local Setup
1. Clone the repository.
2. Ensure you have `uv` installed globally:
   ```bash
   pip install uv