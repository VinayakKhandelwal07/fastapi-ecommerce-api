from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import get_db
from app.routers.auth import get_current_user
from app.schemas import OrderStatus

router = APIRouter(prefix="/orders", tags=["Orders"])


# Route 1: Place an order (User only)
@router.post("/place_order", response_model=schemas.Order)
def place_order(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    cart_items = crud.get_cart_items(db, current_user.id)
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    order = crud.create_order(db, current_user.id)
    if not order:
        raise HTTPException(status_code=400, detail="Order creation failed")
    
    return order


# Route 2: Get orders (User sees their own, Admin sees all)
@router.get("/user_orders", response_model=list[schemas.Order])
def get_orders(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.is_admin:
        return crud.get_all_orders(db)
    return crud.get_orders(db, current_user.id)


# Route 3: View a specific order
@router.get("/order/{order_id}", response_model=schemas.Order)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if not current_user.is_admin and order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this order")

    return order


# Route 4: Update order status (Admin only)
@router.put("/order/{order_id}/status", response_model=schemas.Order)
def update_order_status(
    order_id: int,
    status: OrderStatus,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admin can update order status")

    order = crud.get_orders(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return crud.update_order_status(db, order_id, status)
