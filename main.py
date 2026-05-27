from api_client import fetch_game_details
from models import Game
from database import SessionLocal

def check_discounts():
    """
    Fetches games from the database, checks live prices,
    and updates the database with new current prices.
    """

    print("--- Steam Radar: Database Mode ---")

    db = SessionLocal()

    games = db.query(Game).all()

    for game in games:
        print(f"Checking Steam store for {game.title}...")

        live_price_uah = fetch_game_details(game.app_id)

        if live_price_uah is not None:
            game.current_price = live_price_uah

            discount_percent = game.calculate_discount_percent()

            if discount_percent > 0:
                print(f"Sale on {game.title}! Discount: {discount_percent}%. New price: {game.current_price}₴")
            else:
                print(f"No discount for {game.title}! Current price: {game.current_price}₴")
        else:
            print(f"[!] Could not fetch price for '{game.title}'.")

        print("-")

    print("Committing changes to the database...")
    db.commit()
    db.close()

if __name__ == "__main__":
    check_discounts()