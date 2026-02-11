import io
import os
import random
from datetime import datetime, timedelta

from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from PIL import Image
from passlib.context import CryptContext
from pydantic import BaseModel
from dotenv import load_dotenv
import uvicorn
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from database import SessionLocal, engine, Base
from models import User
from inference import predict_image

# ----------------------------
# Load environment
# ----------------------------
load_dotenv()

MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")
SECRET_KEY = os.getenv("SECRET_KEY")

if not MAIL_USERNAME or not MAIL_PASSWORD or not SECRET_KEY:
    raise RuntimeError("MAIL_USERNAME, MAIL_PASSWORD, or SECRET_KEY not set")

# ----------------------------
# Mail configuration
# ----------------------------
conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_FROM,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

# ----------------------------
# Pydantic models
# ----------------------------
class SendOtpRequest(BaseModel):
    username: str
    password: str
    email: str

class VerifyOtpRequest(BaseModel):
    email: str
    otp: str

# ----------------------------
# App setup
# ----------------------------
app = FastAPI(title="Air Quality Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
Base.metadata.create_all(bind=engine)

# ----------------------------
# Configs
# ----------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
ACCESS_TOKEN_EXPIRE_MINUTES = 60
otp_store = {}  # temporary OTP storage

# ----------------------------
# DB dependency
# ----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------------------------
# JWT helpers
# ----------------------------
def create_access_token(username: str):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({"sub": username, "exp": expire}, SECRET_KEY, algorithm="HS256")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# ----------------------------
# Routes
# ----------------------------
@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")

# ----------------------------
# OTP registration
# ----------------------------
@app.post("/register/send-otp")
async def send_registration_otp(req: SendOtpRequest):
    print("✅ Received OTP request:", req.dict())
    otp = str(random.randint(100000, 999999))
    otp_store[req.email] = {
        "otp": otp,
        "username": req.username,
        "password": req.password,
        "expires": datetime.utcnow() + timedelta(minutes=5)
    }

    message = MessageSchema(
        subject="Your Registration OTP",
        recipients=[req.email],
        body=f"Your verification code is: {otp}",
        subtype="plain"
    )
    try:
        fm = FastMail(conf)
        await fm.send_message(message)
    except Exception as e:
        print("❌ Email sending failed:", e)
        raise HTTPException(status_code=500, detail="Could not send OTP email")
    return {"message": "OTP sent to email"}

@app.post("/register/verify-otp")
async def verify_registration_otp(req: VerifyOtpRequest, db: Session = Depends(get_db)):
    record = otp_store.get(req.email)
    if not record:
        return {"success": False, "message": "No OTP request found"}

    # Ensure expires is a datetime object
    expires = record["expires"]
    if isinstance(expires, str):
        try:
            expires = datetime.fromisoformat(expires)
        except ValueError:
            # fallback if string is not ISO format
            expires = datetime.strptime(expires, "%Y-%m-%d %H:%M:%S.%f")

    # Check if OTP expired
    if datetime.utcnow() > expires:
        del otp_store[req.email]
        return {"success": False, "message": "OTP expired"}

    # Check if OTP matches
    if record["otp"] != req.otp:
        return {"success": False, "message": "Invalid OTP"}

    # OTP correct → create user in DB
    # Truncate password to 72 bytes for bcrypt
    MAX_BCRYPT_BYTES = 72
    password_bytes = record["password"].encode("utf-8")[:MAX_BCRYPT_BYTES]
    safe_password = password_bytes.decode("utf-8", errors="ignore")
    hashed_password = pwd_context.hash(safe_password)

    new_user = User(
        username=record["username"],
        email=req.email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Remove OTP from store
    del otp_store[req.email]

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
# Image prediction
# ----------------------------
@app.post("/predict")
async def predict(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    temp_path = "temp_upload.jpg"
    image.save(temp_path)
    pred_dict = predict_image(temp_path)
    return {"filename": file.filename, "predictions": pred_dict}

# ----------------------------
# Run
# ----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
