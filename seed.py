from database import SessionLocal
from models import Game

def seed_database():
    print("Opening database session...")
    db = SessionLocal()

    game1 = Game(title="The Coma 2: Vicious Sisters", app_id="1045700", base_price=400)
    game2 = Game(title="Red Dead Redemption 2", app_id="1174180", base_price=2600)
    game3 = Game(title="Tales of Arise", app_id="740130", base_price=1500)

    db.add(game1)
    db.add(game2)
    db.add(game3)

    print("Committing changes to the database...")
    db.commit()

    print("Database commited!")
    db.close()

if __name__ == '__main__':
    seed_database()