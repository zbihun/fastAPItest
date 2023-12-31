from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Category(Enum):
    TOOLS = 'tools'
    CONSUMABLES = 'consumables'


class Item(BaseModel):
    name: str
    price: float
    count: int
    id: int
    category: Category


items = {
    0: Item(name="Hammer", price=9.99, count=20, id=0, category=Category.TOOLS),
    1: Item(name="Pliers", price=5.99, count=20, id=1, category=Category.TOOLS),
    2: Item(name="Nails", price=1.99, count=100, id=2, category=Category.CONSUMABLES),
}


@app.get("/")
def index() -> dict[str, dict[int, Item]]:
    return {"items": items}

@app.get("/items/{item_id}")
def query_item_by_id(item_id: int) -> Item:
    if item_id not in items:
        return HTTPException(status_code=404)

    return items[item_id]

Selection = dict[str, str | int | float |Category | None]

@app.get("/items")
def query_item_by_parameters(
    name: str | None = None, 
    price: float | None = None,
    count: int | None = None,
    category: Category | None = None
) -> dict[str, Selection | list]:
    
    def check_item(item: Item) -> bool:
        return all(
            (
                name is None or item.name == name,
                price is None or item.price == price,
                count is None or item.count != count,
                category is None or item.category is category
            )
        )
    
    selection = [item for item in items.values() if check_item(item=item)]
    return {
        "query": {"name": name, "price": price, "count": count, "category": category},
        "selection": selection
    }

@app.post("/")
def add_item(item: Item) -> dict[str, Item]:
    if item.id in items:
        return HTTPException(status_code=400, detail="item with this id already exists")
    
    items[item.id] = item
    return {"added": item}
