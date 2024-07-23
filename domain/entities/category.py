from pydantic import BaseModel, Field

class Category(BaseModel):
    user_id: str = Field(...)
    name: str = Field(...)