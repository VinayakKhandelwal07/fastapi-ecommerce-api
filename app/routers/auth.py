import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import SessionLocal
from app.models import User


# Load environment variables from .env file
load_dotenv()

# --- Password hashing setup ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a plain-text password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify that a plain-text password matches the hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

# --- JWT Token settings ---
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable not set")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a JWT token with an expiration time."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- FastAPI router and dependencies ---
router = APIRouter()

def get_db():
    """Dependency to get DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# --- Auth API endpoints ---
@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Register a new user with a unique username."""
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed_pw = hash_password(user.password)
    return crud.create_user(db, schemas.UserCreate(username=user.username, email=user.email, password=user.password, hashed_password=hashed_pw))


ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_HASHED_PASSWORD = os.getenv("ADMIN_HASHED_PASSWORD")
if not ADMIN_HASHED_PASSWORD:
    raise ValueError("ADMIN_HASHED_PASSWORD not set in environment variables")



@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Login user by verifying credentials and returning a JWT token.
    Accepts form data for compatibility with Swagger UI OAuth2.
    """
     # --- Admin Login Check ---
    if form_data.username == ADMIN_USERNAME:
        if not verify_password(form_data.password, ADMIN_HASHED_PASSWORD):
            raise HTTPException(status_code=400, detail="Invalid admin credentials")

        # Create admin token
        access_token = create_access_token(data={
            "sub": ADMIN_USERNAME,
            "role": "admin" 
        })
        return {"access_token": access_token, "token_type": "bearer"}
    

    db_user = crud.get_user_by_username(db, form_data.username)
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """Decode JWT token, verify user exists, and return current user object."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        role: str | None = payload.get("role")
        if username is None:
            raise credentials_exception
        
          # If admin token
        if role == "admin" and username == ADMIN_USERNAME:
            admin_user = User(
                id=0,
                username=ADMIN_USERNAME,
                email="admin@example.com",
                hashed_password=ADMIN_HASHED_PASSWORD,
                is_admin=True
            )
            return admin_user
        
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise credentials_exception
    return user


def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return current_user


@router.get("/me", response_model=schemas.UserOut)
def read_profile(current_user: User = Depends(get_current_user)):
    """Return the profile of the logged-in user."""
    return current_user
