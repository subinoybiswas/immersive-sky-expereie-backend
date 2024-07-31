from pydantic import BaseModel, Field, BeforeValidator, EmailStr, ConfigDict
from typing import Optional, Annotated


# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]


class UserBase(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None) # This will be aliased to `_id` when sent to MongoDB, but provided as `id` in the API requests and responses.
    username: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    role: str = Field(default="user") # like admin, user
    model_config = ConfigDict(
        populate_by_name=True, # Populate the model with the values from the JSON by name (e.g. `{"name": "Jane Doe"}` will populate the `name` field)
        arbitrary_types_allowed=True, # Allow arbitrary types to be passed in the JSON (e.g. `datetime`, `ObjectId`, etc.)
        json_schema_extra={
            "example": {
                "username": "johndoe",
                "email": "john@example.com",
                "password": "password",
                "role": "user"
            }
        },
    )



# AUTH MODELS

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    role: str

class TokenData(BaseModel):
    username: str = None


