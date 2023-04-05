import uuid
from typing import Optional
from pydantic import BaseModel, validator


class User(BaseModel):
    id: str = uuid.uuid4().__str__()
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[str] = None
    age: int

    @validator('first_name')
    def validate_first_name(cls, value: Optional[str], values):
        if value is None:
            raise ValueError('First name is required')
        if not value.isalpha():
            raise ValueError('First name must only contain alphabets')
        if len(value) > 30:
            raise ValueError('First name must not be greater than 30 letters')
        return value

    @validator('last_name')
    def validate_last_name(cls, value: Optional[str], values):
        if value is None:
            raise ValueError('Last name is required')
        if not value.isalpha():
            raise ValueError('Last name must only contain alphabets')
        if len(value) > 30:
            raise ValueError('Last name must not be greater than 30 letters')
        return value

    @validator('gender')
    def validate_gender(cls, value: Optional[str], values):
        if value is None:
            raise ValueError('Gender is required')
        if value.lower() not in ['male', 'female', 'other']:
            raise ValueError('Gender must be one of ["male","female","other"]')
        return value

    @validator('age')
    def validate_age(cls, value: int):
        if value < 18:
            raise ValueError('Age must be greater than or equal to 18')
        return value
