from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.schemas import ProductCreate, ProductUpdate, ProductOut
from app.crud import get_products, get_product, create_product, update_product, delete_product
from app.database import SessionLocal
from app.routers.auth import get_current_user  # your existing auth function
from app.models import User

router = APIRouter(prefix="/products", tags=["Products"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Optional: Admin-check dependency
def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user

@router.get("/", response_model=List[ProductOut])
def read_products(
    skip: int = 0,
    limit: int = Query(20, le=100),
    search: str = Query(None, description="Search products by name/description"),
    db: Session = Depends(get_db)
):
    return get_products(db, skip=skip, limit=limit, search=search)

@router.get("/{product_id}", response_model=ProductOut)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_new_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    return create_product(db, product)

@router.put("/{product_id}", response_model=ProductOut)
def update_existing_product(
    product_id: int,
    updates: ProductUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    db_product = get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return update_product(db, db_product, updates)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_product(
    product_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    db_product = get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    delete_product(db, db_product)
    return
