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
```
2. Create and Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```
3. Install Requirements
```bash
pip install -r requirements.txt
```
4. Run the Server
```bash

uvicorn app.main:app --reload
API docs available at http://127.0.0.1:8000/docs
```
🔑 API Authentication

Auth is handled via OAuth2 Password Flow using form-data.

After logging in, use the returned JWT token as a Bearer token in headers:
```bash
Authorization: Bearer <your_token>
```
🧪 Testing the API
You can test endpoints via:

🔥 Swagger UI at /docs

🧪 Thunder Client or Postman


📂 Project Structure
```bash

app/
├── main.py               # FastAPI entry point
├── models.py             # SQLAlchemy models
├── schemas.py            # Pydantic schemas
├── crud.py               # Database operations
├── routes/               # API route definitions
├── auth/                 # Auth & token logic
└── database.py           # DB config
```
📬 Contact

Vinayak Khandelwal

📧 [khandelwalvinayak84@gmail.com]

🌐https://www.linkedin.com/in/vinayak-khandelwal-b3216425a/

🪪 License

This project is licensed under the MIT License.
