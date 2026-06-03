from pydantic import BaseModel, ConfigDict

class GameCreate(BaseModel):
    title: str
    app_id: str
    base_price: int

class GameResponse(BaseModel):
    id: int
    title: str
    app_id: str
    base_price: int
    current_price: int

    model_config = ConfigDict(from_attributes=True)


