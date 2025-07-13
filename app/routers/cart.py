from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import schemas, crud
from app.database import SessionLocal
from app.routers.auth import get_current_user
from app.models import User

router = APIRouter(prefix="/cart", tags=["Cart"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.CartItemOut])
def read_cart_items(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    items = crud.get_cart_items(db, current_user.id)
    # enrich with product name for response
    for item in items:
        item.product_name = item.product.name
    return items

@router.post("/", response_model=schemas.CartItemOut, status_code=status.HTTP_201_CREATED)
def add_to_cart(item: schemas.CartItemCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    product = crud.get_product(db, item.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    cart_item = crud.add_cart_item(db, current_user.id, item.product_id, item.quantity)
    cart_item.product_name = product.name
    return cart_item

@router.put("/{product_id}", response_model=schemas.CartItemOut)
def update_cart_item_quantity(product_id: int, update: schemas.CartItemUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cart_item = crud.update_cart_item(db, current_user.id, product_id, update.quantity)
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    cart_item.product_name = cart_item.product.name
    return cart_item

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_cart(product_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    crud.remove_cart_item(db, current_user.id, product_id)
    return
