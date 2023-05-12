from typing import Union

from pydantic import BaseModel


class Category(BaseModel):
    name: str

    class Config:
        orm_mode = True


class MovieWrite(BaseModel):
    url: str
    comment: str
    rating: int

    class Config:
        orm_mode = True


class Movie(BaseModel):
    id: int
    title: str
    published_at: Union[str, None] = None
    total_audience: Union[str, None] = None
    running_time: Union[str, None] = None
    rating: Union[int, None] = None
    comment: str

    class Config:
        orm_mode = True
