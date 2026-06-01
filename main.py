from fastapi import FastAPI, HTTPException
from requests import session

from database import SessionLocal
from models import Game
from api_client import fetch_game_details

app = FastAPI(title= "Steam Discount Analytics API")

@app.get("/")
def read_root():
    return {"message": "Welcome to Steam Discount Analytics API!"}

@app.get("/games")
def read_all_games():
    db = SessionLocal()
    try:
        games = db.query(Game).all()
        return games
    finally:
        db.close()

@app.get("/games/{app_id}")
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