Steam Discount Analytics API
A modern, high-performance backend service designed to track Steam wishlist game prices, analyze discounts, and automate data synchronization. Built with a focus on modern Python development standards.

Features
Automated Price Tracking: Built-in background scheduler automatically fetches and updates game prices from Steam every 12 hours.

RESTful API: Full CRUD functionality to manage tracked games, dynamically interact with the database, and trigger manual updates.

Data Validation: Strict input/output validation and serialization using Pydantic schemas.

Asynchronous Execution: Non-blocking background tasks for mass price updates to ensure high API responsiveness.

Containerized: Fully ready for production deployment with Docker and Docker Compose.

Tech Stack
Framework: FastAPI

Package Manager: uv (Extremely fast Python package installer and resolver written in Rust)

Database & ORM: SQLite + SQLAlchemy

Data Validation: Pydantic

Task Scheduling: APScheduler

Containerization: Docker & Docker Compose

API Endpoints
The API provides interactive documentation via Swagger UI. Once the server is running, navigate to /docs to explore and test the endpoints.

Games Management
GET /games - Retrieve a list of all tracked games.

POST /games - Add a new game to the tracking list.

GET /games/{app_id} - Retrieve details of a specific game.

DELETE /games/{app_id} - Remove a game from the tracking list.

Synchronization & Updates
POST /games/{app_id}/update-price - Instantly fetch and update the price for a specific game from Steam.

POST /games/update-all - Trigger a background worker to mass-update prices for all tracked games.

Getting Started
You can run this project either directly on your local machine using uv, or inside an isolated Docker container.

Option 1: Local Development (Using uv)
Clone the repository:
git clone 
cd SteamDiscountAnalytics

Install uv (if not already installed):
pip install uv

Install dependencies and sync the environment:
uv sync

Run the FastAPI development server:
uv run uvicorn main:app --reload --port 8080

The API will be available at http://127.0.0.1:8080

Option 2: Production (Using Docker Compose)
Ensure Docker Desktop is running.

Build and start the container:
docker-compose up --build

The API will be available at http://localhost:8080
To stop the container, press Ctrl+C in the terminal or run docker-compose down.