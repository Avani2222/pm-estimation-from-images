import io
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta
from PIL import Image
from passlib.context import CryptContext

from inference import predict_image, LABEL_COLS
from database import SessionLocal, engine, Base
from models import User
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from datetime import datetime, timedelta
import random

conf = ConnectionConfig(
    MAIL_USERNAME="avanigupta2003@gmail.com",
    MAIL_PASSWORD="fltu hxlb iwnl ifxt",
    MAIL_FROM="avanigupta2003@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

otp_store = {}  # temporary storage

# ----------------------------
# Create tables if not exists
# ----------------------------
Base.metadata.create_all(bind=engine)

# ----------------------------
# Configs
# ----------------------------
UNITS = {
    'AQI': '',
    'PM2.5': 'µg/m³',
    'PM10': 'µg/m³',
    'O3': 'ppb',
    'CO': 'ppm',
    'SO2': 'ppb',
    'NO2': 'ppb'
}

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# ----------------------------
# FastAPI app
# ----------------------------
app = FastAPI(title="Air Quality Prediction API")

# ----------------------------
# CORS
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to your frontend URL in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# Serve static folder
# ----------------------------
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")


# ----------------------------
# Database dependency
# ----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ----------------------------
# Auth helpers
# ----------------------------
def create_access_token(username: str):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = jwt.encode({"sub": username, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
    return token


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# ----------------------------
# User registration
# ----------------------------
@app.post("/register")
def register(username: str, password: str, email: str = None, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(password)
    user = User(username=username, hashed_password=hashed_password, email=email)
    db.add(user)
    try:
        db.commit()
        db.refresh(user)
    except:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username or email already exists")
    return {"message": "User registered successfully!"}

@app.post("/register/send-otp")
async def send_registration_otp(username: str, email: str, password: str):

    otp = str(random.randint(100000, 999999))

    otp_store[email] = {
        "otp": otp,
        "username": username,
        "password": password,  # will hash later
        "expires": datetime.now() + timedelta(minutes=5)
    }

    message = MessageSchema(
        subject="Your Registration OTP",
        recipients=[email],
        body=f"Your verification code is: {otp}",
        subtype="plain"
    )

    fm = FastMail(conf)
    await fm.send_message(message)

    return {"message": "OTP sent to email"}

@app.post("/register/verify-otp")
async def verify_registration_otp(email: str, otp: str):

    record = otp_store.get(email)

    if not record:
        return {"success": False, "message": "No OTP request found"}

    if datetime.now() > record["expires"]:
        return {"success": False, "message": "OTP expired"}

    if record["otp"] != otp:
        return {"success": False, "message": "Invalid OTP"}

    # OTP correct → create user
    hashed_password = pwd_context.hash(record["password"])

    # SAVE TO DATABASE HERE
    # Example:
    # new_user = User(username=record["username"], email=email, password=hashed_password)
    # db.add(new_user)
    # db.commit()

    del otp_store[email]  # cleanup

    return {"success": True, "message": "Registration complete"}

# ----------------------------
# User login
# ----------------------------
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    token = create_access_token(user.username)
    return {"access_token": token, "token_type": "bearer"}


# ----------------------------
# Prediction API (protected)
# ----------------------------
@app.post("/predict")
async def predict(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")

    temp_path = "temp_upload.jpg"
    image.save(temp_path)

    pred_dict = predict_image(temp_path)

    # Convert predictions to string with units

    return {
        "filename": file.filename,
        "predictions": pred_dict
    }