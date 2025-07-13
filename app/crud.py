from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app import models, schemas
from app.utils import hash_password
from app.models import Order, OrderItem, OrderStatus, Product, CartItem
from app.schemas import ProductCreate, ProductUpdate


# ---------------------- User CRUD ----------------------

def create_user(db: Session, user: schemas.UserCreate):
    hashed_pw = hash_password(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pw,
        is_admin=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


# ---------------------- Product CRUD ----------------------

def get_products(db: Session, skip: int = 0, limit: int = 100, search: str = None):
    query = db.query(Product)
    if search:
        search = f"%{search.lower()}%"
        query = query.filter(or_(
            Product.name.ilike(search),
            Product.description.ilike(search)
        ))
    return query.offset(skip).limit(limit).all()

def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def create_product(db: Session, product: ProductCreate):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, db_product: Product, updates: ProductUpdate):
    update_data = updates.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, db_product: Product):
    db.delete(db_product)
    db.commit()


# ---------------------- Cart CRUD ----------------------

def get_cart_items(db: Session, user_id: int):
    return db.query(CartItem).filter(CartItem.user_id == user_id).all()

def get_cart_item(db: Session, user_id: int, product_id: int):
    return db.query(CartItem).filter(
        CartItem.user_id == user_id,
        CartItem.product_id == product_id
    ).first()

def add_cart_item(db: Session, user_id: int, product_id: int, quantity: int = 1):
    item = get_cart_item(db, user_id, product_id)
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if item:
        item.quantity += quantity
        item.price = product.price  # ✅ update price snapshot
    else:
        item = CartItem(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity,
            price=product.price
        )
        db.add(item)

    db.commit()
    db.refresh(item)
    return schemas.CartItemOut(
        id=item.id,
        product_id=item.product_id,
        quantity=item.quantity,
        price=item.price,
        product_name=item.product.name  # access via relationship
    )

def update_cart_item(db: Session, user_id: int, product_id: int, quantity: int):
    item = get_cart_item(db, user_id, product_id)
    if item:
        item.quantity = quantity
        db.commit()
        db.refresh(item)
    return item

def remove_cart_item(db: Session, user_id: int, product_id: int):
    item = get_cart_item(db, user_id, product_id)
    if item:
        db.delete(item)
        db.commit()


# ---------------------- Order CRUD ----------------------

def create_order(db: Session, user_id: int):
    cart_items = db.query(CartItem).filter(CartItem.user_id == user_id).all()
    if not cart_items:
        return None

    # ✅ Stock check
    for item in cart_items:
        if item.product.stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for product: {item.product.name}"
            )

    # ✅ Use CartItem price snapshot
    total_price = sum(item.price * item.quantity for item in cart_items)

    order = Order(user_id=user_id, total_price=total_price)
    db.add(order)
    db.commit()
    db.refresh(order)

    # ✅ Create order items and update stock
    for item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.price
        )
        db.add(order_item)

        # ✅ Update stock
        item.product.stock -= item.quantity

    # ✅ Clear cart
    for item in cart_items:
        db.delete(item)

    db.commit()
    return order


def get_orders(db: Session, user_id: int):
    return db.query(Order).filter(Order.user_id == user_id).all()

def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()

def update_order_status(db: Session, order_id: int, status: OrderStatus):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        order.status = status
        db.commit()
        db.refresh(order)
    return order

def get_all_orders(db: Session):
    return db.query(Order).all()
