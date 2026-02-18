from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)

class PollutionData(Base):
    __tablename__ = "pollution_data"

    id = Column(Integer, primary_key=True)
    latitude = Column(Float)
    longitude = Column(Float)
    aqi = Column(Float)
    pm25 = Column(Float)
    pm10 = Column(Float)
    o3 = Column(Float)
    co = Column(Float)
    so2 = Column(Float)
    no2 = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)