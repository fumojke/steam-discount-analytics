from database import SessionLocal
from models import Game

def view_games():
    db = SessionLocal()

    games = db.query(Game).all()

    print("--- Games in Database ---")
    if not games:
        print("Database is empty!")
    else:
        for game in games:
            print(f"Title {game.title} | AppID: {game.app_id} | Base Price: {game.base_price} ₴")

    db.close()

if __name__ == "__main__":
    view_games()