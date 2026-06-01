from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Game(Base):
    """Represents a video game table in the database."""

    __tablename__ = 'games'

    # primary_key=True
    id = Column(Integer, primary_key=True)

    # nullable=False
    title = Column(String,nullable=False)

    # unique=True
    app_id = Column(String, unique=True, nullable=False)
    base_price = Column(Integer, nullable=False)

    # The current default price is 0
    current_price = Column(Integer, default=0)

    def calculate_discount_percent(self):
        """Calculates and returns the discount percentage."""
        if self.current_price < self.base_price:
            return int((self.base_price - self.current_price) / self.base_price * 100)
        return 0


