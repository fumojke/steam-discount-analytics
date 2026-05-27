import time
from api_client import fetch_wishlist, fetch_game_details
from database import SessionLocal
from models import Game

def sync_user_wishlist(steam_id):
    print(f"Starting sync wishlist for SteamID {steam_id}")

    wishlist_items = fetch_wishlist(steam_id)

    if not wishlist_items:
        print("[!] No items found or profile is private")
        return

    wishlist_items = wishlist_items[:5]
    db = SessionLocal()

    for item in wishlist_items:
        app_id = str(item['appid'])
        print(f"Processing AppID {app_id}...")

        details = fetch_game_details(app_id)

        if details:
            game_title = details['title']
            game_price = details['price']

            print(f"Found: {game_title} - {game_price} ₴")

            existing_game = db.query(Game).filter(Game.app_id == app_id).first()

            if not existing_game:
                # Четко указываем: title=..., app_id=...
                new_game = Game(title=game_title, app_id=app_id, base_price=game_price)

                db.add(new_game)
                print(f"Added: {game_title} to database.")
            else:
                print(f"Game {game_title} already exists in database. Skipping...")

        time.sleep(1.5)

    print("Committing changes...")
    db.commit()
    db.close()
    print("Synchronization complete!")


if __name__ == "__main__":
    my_steam_id = "76561198132789707"
    sync_user_wishlist(my_steam_id)