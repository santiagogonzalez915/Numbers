from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from passlib.context import CryptContext

DATABASE_URL = "sqlite:///./numbers.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    stats = relationship("UserStats", back_populates="user", uselist=False)

class UserStats(Base):
    __tablename__ = "user_stats"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    games_played = Column(Integer, default=0)
    games_won = Column(Integer, default=0)
    average_moves = Column(Float, default=0.0)
    best_time = Column(Float, nullable=True)
    average_time = Column(Float, default=0.0)
    longest_win_streak = Column(Integer, default=0)
    current_win_streak = Column(Integer, default=0)
    total_moves = Column(Integer, default=0)
    user = relationship("User", back_populates="stats")

# Create tables
Base.metadata.create_all(bind=engine) 