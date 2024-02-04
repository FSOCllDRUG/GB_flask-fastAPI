import datetime
import json
from random import randint

from fastapi import FastAPI, HTTPException
from starlette.responses import HTMLResponse

import database as db
import models

app = FastAPI()


@app.get("/")
def root():
    return {"Message": "Hello"}


@app.get("/fake_users/{count}")
async def create_note(count: int):
    for i in range(count):
        query = db.users.insert().values(Имя=f'Имя{i}', Фамилия=f'Фамилия{i}', email=f'mail{i}@mail.com',
                                         password=f'1234567890{i}')
        await db.database.execute(query)
    return {'message': f'{count} fake users generated'}


@app.get("/fake_products/{count}")
async def create_note(count: int):
    for i in range(count):
        query = db.products.insert().values(Название=f'Товар{i}', Описание=f'Текст{i}',
                                            Цена=randint(1, 100000))
        await db.database.execute(query)
    return {'message': f'{count} fake products generated'}


@app.get("/fake_orders/{count}")
async def create_note(count: int):
    for i in range(count):
        query = db.orders.insert().values(user_id=randint(1, 20), prod_id=randint(1, 20), Статус_заказа="Создан",
                                          Дата_заказа=datetime.datetime.now())
        await db.database.execute(query)
    return {'message': f'{count} fake orders generated'}


# Read all

@app.get("/users/", response_class=HTMLResponse)
async def read_users():
    query = db.users.select()
    users = await db.database.fetch_all(query)
    formatted_users = json.dumps([dict(user) for user in users], ensure_ascii=False, indent=4)
    return formatted_users.replace('\n', '<br>')


@app.get("/products/", response_class=HTMLResponse)
async def read_products():
    query = db.products.select()
    products = await db.database.fetch_all(query)
    formatted_products = json.dumps([dict(product) for product in products], ensure_ascii=False, indent=4)
    return formatted_products.replace('\n', '<br>')


@app.get("/orders/", response_class=HTMLResponse)
async def read_orders():
    query = db.orders.select()
    orders = await db.database.fetch_all(query)
    formatted_orders = []
    for order in orders:
        order_dict = dict(order)
        if 'Дата_заказа' in order_dict and order_dict['Дата_заказа']:
            order_dict['Дата_заказа'] = order_dict['Дата_заказа'].strftime("%Y-%m-%d %H:%M:%S")
        formatted_orders.append(order_dict)
    return json.dumps(formatted_orders, ensure_ascii=False, indent=4).replace('\n', '<br>')


# Read only one

@app.get("/users/{user_id}", response_model=models.UserRead)
async def read_user(user_id: int):
    query = db.users.select().where(db.users.c.id == user_id)
    user = await db.database.fetch_one(query)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/products/{product_id}", response_model=models.ProductRead)
async def read_product(product_id: int):
    query = db.products.select().where(db.products.c.id == product_id)
    product = await db.database.fetch_one(query)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.get("/orders/{order_id}", response_model=models.OrderRead)
async def read_order(order_id: int):
    query = db.orders.select().where(db.orders.c.id == order_id)
    order = await db.database.fetch_one(query)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    order_dict = dict(order)
    order_dict["Дата_заказа"] = order_dict["Дата_заказа"].isoformat()
    return order_dict


# update user/product/order

@app.put("/users/{user_id}", response_model=models.UserRead)
async def update_user(user_id: int, new_user: models.UserCreate):
    query = db.users.update().where(db.users.c.id == user_id).values(**new_user.dict())
    await db.database.execute(query)
    return {**new_user.dict(), "id": user_id}


@app.put("/products/{product_id}", response_model=models.ProductRead)
async def update_product(product_id: int, new_product: models.ProductCreate):
    query = db.products.update().where(db.products.c.id == product_id).values(**new_product.dict())
    await db.database.execute(query)
    return {**new_product.dict(), "id": product_id}


@app.put("/orders/{order_id}", response_model=models.OrderRead)
async def update_order(order_id: int, new_order: models.OrderCreate):
    query = db.orders.update().where(db.orders.c.id == order_id).values(**new_order.dict())
    await db.database.execute(query)
    return {**new_order.dict(), "id": order_id}


# Delete one

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = db.users.delete().where(db.users.c.id == user_id)
    await db.database.execute(query)
    return {'message': 'User deleted'}


@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    query = db.products.delete().where(db.products.c.id == product_id)
    await db.database.execute(query)
    return {'message': 'Product deleted'}


@app.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    query = db.orders.delete().where(db.orders.c.id == order_id)
    await db.database.execute(query)
    return {'message': 'Order deleted'}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
