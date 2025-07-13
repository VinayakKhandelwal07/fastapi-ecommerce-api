🛒 FastAPI E-Commerce Backend API

A high-performance, scalable **E-Commerce REST API** built with **FastAPI**, implementing secure user authentication, product management, cart functionality, and order processing.

This project demonstrates a solid understanding of modern backend design, including **JWT-based authentication**, **ORM with SQLAlchemy**, and **API documentation with Swagger**.

---

🚀 Features

- ✅ **User Authentication & Authorization**
  - Secure registration and login with hashed passwords
  - JWT-based authentication
  - Admin support for privileged routes

- 🛍️ **Product Management (Admin only)**
  - Create, update, delete, and list products
  - Image URL and stock management

- 🛒 **Shopping Cart**
  - Add, update, remove products
  - Price snapshot saved at time of addition

- 📦 **Order System**
  - Place orders from cart
  - Real-time stock validation and reduction
  - Order history and individual order retrieval

- 📘 **Interactive API Docs**
  - Auto-generated Swagger UI and ReDoc at:
    - `/docs`
    - `/redoc`

---

🛠️ Tech Stack

| Layer            | Technology       |
|------------------|------------------|
| API Framework    | FastAPI          |
| ORM              | SQLAlchemy       |
| Database         | SQLite (Dev)     |
| Auth             | OAuth2 + JWT     |
| Password Hashing | Passlib (bcrypt) |
| Docs             | Swagger / ReDoc  |

---

⚙️ Setup Instructions

1. Clone the Repository

```bash
git clone https://github.com/VinayakKhandelwal07/fastapi-ecommerce-api.git
cd fastapi-ecommerce-api


