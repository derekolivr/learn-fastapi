from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List
from database import SessionLocal
import models


app = FastAPI()


class Item(BaseModel):
    id: int
    name: str
    description: str
    price: int
    on_offer: bool

    class Config:
        orm_mode = True


db = SessionLocal()


@app.get("/items", response_model=List[Item], status_code=200)
def get_all_items():
    items = db.query(models.Item).all()

    return items


@app.get("/items/{item_id}", response_model=Item, status_code=status.HTTP_200_OK)
def get_an_item(item_id: int):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    return item


@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_an_item(item: Item):
    new_item = models.Item(
        id=item.id,
        name=item.name,
        price=item.price,
        description=item.description,
        on_offer=item.on_offer,
    )

    db_items = db.query(models.Item).filter(models.Item.name == new_item.name).first()

    if db_items is not None:
        raise HTTPException(status_code=400, detail="Item already exists")

    db.add(new_item)
    db.commit()

    return new_item


@app.put("/items/{item_id}", response_model=Item, status_code=status.HTTP_200_OK)
def update_an_item(item_id: int, updated_item: Item):
    item_to_update = db.query(models.Item).filter(models.Item.id == item_id).first()

    if item_to_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found"
        )

    item_to_update.name = updated_item.name
    item_to_update.price = updated_item.price
    item_to_update.description = updated_item.description
    item_to_update.on_offer = updated_item.on_offer

    db.commit()

    return item_to_update


@app.delete("/items/{item_id}")
def delete_an_item(item_id: int):
    item_to_delete = db.query(models.Item).filter(models.Item.id == item_id).first()

    if item_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found"
        )

    db.delete(item_to_delete)
    db.commit()

    return item_to_delete


"""
@app.get("/")
def index():
    return {"message": "hello world!"}


@app.get("/berate/{name}")
def berate(name: str):
    return {"greeting": f"You suck {name}"}


@app.get("/berate")
def berate(name: Optional[str] = "User"):
    return {"greeting": f"You suck {name}"}


@app.put("/item/{item_id}")
def update_item(item_id: int, item: Item):
    return {
        "name": item.name,
        "description": item.description,
        "price": item.price,
    }

"""
