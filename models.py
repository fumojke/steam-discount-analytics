from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

# Создаем базовый класс, от которого будут наследоваться все наши таблицы
Base = declarative_base()


class Game(Base):
    """Represents a video game table in the database."""

    # Указываем имя таблицы в базе данных
    __tablename__ = 'games'

    # Описываем колонки:
    # primary_key=True означает, что это уникальный номер строки (ID)
    id = Column(Integer, primary_key=True)

    # nullable=False означает, что это поле не может быть пустым
    title = Column(String,nullable=False)

    # unique=True гарантирует, что мы не добавим одну и ту же игру дважды
    app_id = Column(String, unique=True, nullable=False)
    base_price = Column(Integer, nullable=False)

    # Текущая цена по умолчанию равна 0
    current_price = Column(Integer, default=0)

    def calculate_discount_percent(self):
        """Calculates and returns the discount percentage."""
        if self.current_price < self.base_price:
            return int((self.base_price - self.current_price) / self.base_price * 100)
        return 0


