from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    
    model_config = ConfigDict(from_attributes=True)

    username: str = Field(..., max_length=64, min_length=4)
    email: str = Field(..., max_length=320, min_length=6)
    first_name: str = Field(..., max_length=64, min_length=2)
    last_name: str = Field(..., max_length=64, min_length=2)


class UserOut(UserBase):
    pass


class UserCreateIn(UserBase):
    hashed_password: str


class UserLoginIn(BaseModel):
    username_or_email: str
    password: str

