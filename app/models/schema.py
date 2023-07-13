from typing import Union
from pydantic import BaseModel

class UserSchema(BaseModel):
    name : str
    email : str
    password : str
    amount: Union[int, float]

