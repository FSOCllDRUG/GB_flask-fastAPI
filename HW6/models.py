from datetime import datetime

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    Имя: str = Field(max_length=32)
    Фамилия: str = Field(max_length=32)
    email: str = Field(max_length=128)
    password: str = Field(min_length=3)


class UserRead(BaseModel):
    id: int
    Имя: str = Field(max_length=32)
    Фамилия: str = Field(max_length=32)
    email: str = Field(max_length=128)
    password: str = Field(min_length=3)


class ProductCreate(BaseModel):
    Название: str = Field(max_length=50)
    Описание: str = Field(max_length=300)
    Цена: int = Field(default=0)


class ProductRead(BaseModel):
    id: int
    Название: str = Field(max_length=50)
    Описание: str = Field(max_length=300)
    Цена: int = Field(default=0)


class OrderCreate(BaseModel):
    user_id: int
    prod_id: int
    Дата_заказа: datetime = Field(default=datetime.now())
    Статус_заказа: str = Field(default="Создан")


class OrderRead(BaseModel):
    id: int
    user_id: int
    prod_id: int
    Дата_заказа: str
    Статус_заказа: str = Field(default="Создан")
