from fastapi import FastAPI
from app.routers import auth
from app import models
from app.database import Base, engine
from app.routers import cart
from app.routers.product import router as product_router
from app.routers.orders import router as order_router  # Importing the orders router

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# Root endpoint
@app.get("/")
def root():
    return {"message": "FastAPI E-commerce Backend is up!"}

# Include auth routes
app.include_router(auth.router)

# Include product routes
app.include_router(product_router)

# Include cart routes
app.include_router(cart.router)

# Include order routes (added)
app.include_router(order_router)  # Registering the orders router
