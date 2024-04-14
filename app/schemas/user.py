from pydantic import (
    BaseModel,
    ConfigDict,
    Field
    )

    

class UserCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    username: str = Field(...,max_length=64,min_length=4)
    slug: str
    email: str = Field(...,max_length=320,min_length=6)
    first_name: str = Field(...,max_length=64,min_length=2)
    last_name: str = Field(...,max_length=64,min_length=2)
    is_verified: bool = False
    hashed_password:str

class UserPrivate(UserCreateSchema):
    hashed_password: str