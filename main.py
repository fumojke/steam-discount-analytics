import time
from typing import List
from fastapi import FastAPI, HTTPException, BackgroundTasks
from database import SessionLocal
from models import Game
from api_client import fetch_game_details
from schemas import GameResponse, GameCreate
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler


def update_all_prices_task():
    db = SessionLocal()
    try:
        games = db.query(Game).all()

        # Add a print to see when the task actually starts
        print("Starting scheduled background update...")

        for game in games:
            fresh_data = fetch_game_details(game.app_id)

            if fresh_data:
                game.current_price = fresh_data["price"]
                db.commit()
                # Print each game as it gets updated
                print(f"Updated price for: {game.title}")

            time.sleep(1.5)

        print("Scheduled background update finished.")
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = BackgroundScheduler()

    # Add our update task to run on an interval
    # NOTE: We use minutes=1 for testing. Later we will change it to hours=12.
    scheduler.add_job(update_all_prices_task, 'interval', hours=12)

    scheduler.start()
    print("Background scheduler started! Auto-updating prices every 1 minute...")

    yield # This is where the FastAPI application actually runs

    scheduler.shutdown()
    print("Background scheduler shut down.")
app = FastAPI(title="Steam Discount Analytics API", lifespan=lifespan)
@app.get("/")
def read_root():
    return {"message": "Welcome to Steam Discount Analytics API!"}

@app.get("/games", response_model=List[GameResponse])
def read_all_games():
    db = SessionLocal()
    try:
        games = db.query(Game).all()
        return games
    finally:
        db.close()

@app.get("/games/{app_id}", response_model=GameResponse)
def read_single_game(app_id: str):
    db = SessionLocal()
    try:
        game = db.query(Game).filter(Game.app_id == app_id).first()
        if not game:
                raise HTTPException(status_code=404, detail="Game not found!")

        return game
    finally:
        db.close()

@app.post("/games/{app_id}/update-price")
def update_game_price(app_id: str):
    db = SessionLocal()
    try:
        game = db.query(Game).filter(Game.app_id == app_id).first()

        if not game:
            raise HTTPException(status_code=404, detail="Game not found!")

        fresh_data = fetch_game_details(app_id)

        if not fresh_data:
            raise HTTPException(status_code=400, detail="Could not fetch data from Steam.")

        game.current_price = fresh_data["price"]

        db.commit()

        db.refresh(game)

        return {
            "message": f"Price updated successfully for {game.title}!",
            "game": game
        }
    finally:
        db.close()

@app.post("/games", response_model=GameResponse, status_code=201)
def create_game(game_in: GameCreate):
    """
    Creates a new game record in the database after validating the input data.
    Returns the newly created game with its generated ID.
    """

    db = SessionLocal()
    try:
        existing_game = db.query(Game).filter(Game.app_id == game_in.app_id).first()
        if existing_game:
            raise HTTPException(status_code=400, detail="Game with this AppID already exists.")

        new_game = Game(
            title=game_in.title,
            app_id=game_in.app_id,
            base_price=game_in.base_price
            # current_price will default to 0 automatically in the DB
        )

        db.add(new_game)
        db.commit()

        db.refresh(new_game)

        return new_game
    finally:
        db.close()

@app.delete("/games/{app_id}", status_code=200)
def delete_game(app_id: str):
    """
    Deletes a game record from the database by its Steam AppID.
    If the game does not exist, raises a 404 error.
    """
    db = SessionLocal()
    try:
        game = db.query(Game).filter(Game.app_id == app_id).first()

        if not game:
            raise HTTPException(status_code=404, detail="Game not found!")

        db.delete(game)
        db.commit()

        return {"message": f"Game {game.title} has been successfully deleted from the database."}
    finally:
        db.close()
# ---------------------------------------------------------
# BACKGROUND TASK LOGIC
# ---------------------------------------------------------

# NEW ROUTE: Mass update using Background Tasks
@app.post("/games/update-all")
def update_all_games(background_tasks: BackgroundTasks):
    background_tasks.add_task(update_all_prices_task)

    return {
        "message": "Mass update started in the background! Please check back in a few minutes."
    }