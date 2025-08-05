import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from backend.core import create  
import uuid
from fastapi.middleware.cors import CORSMiddleware
from backend.api.models import MoveModel, GameStateModel, ResultModel
from pydantic import BaseModel
from backend.core.database import SessionLocal, User, UserStats, get_password_hash
from sqlalchemy.exc import IntegrityError
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from fastapi import Security
from fastapi.security import OAuth2PasswordBearer
from backend.core.database import verify_password
from fastapi import Request
from typing import Optional
from fastapi.security.utils import get_authorization_scheme_param

load_dotenv()
SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY environment variable not set. Please set it in your .env file.")

games = {}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Numbers Game API is running!"}

class NewGameRequest(BaseModel):
    difficulty: int = 1

@app.post("/game/start", response_model=GameStateModel)
def start_game(request: NewGameRequest):
    state = create.createGame(difficulty=request.difficulty)
    game_id = str(uuid.uuid4())
    games[game_id] = state
    state['game_id'] = game_id
    return GameStateModel(**state)

@app.get("/game/{game_id}", response_model=GameStateModel)
def get_game(game_id: str):
    state = games.get(game_id)
    if not state:
        raise HTTPException(status_code=404, detail="Game not found")
    return GameStateModel(**state)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise credentials_exception
        return user
    finally:
        db.close()

def get_token_optional(request: Request):
    auth = request.headers.get("Authorization")
    if not auth:
        return None
    scheme, param = get_authorization_scheme_param(auth)
    if scheme.lower() != "bearer":
        return None
    return param


def get_current_user_optional(token: str = Depends(get_token_optional)):
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
    except JWTError:
        return None
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            return None
        return user
    finally:
        db.close()

@app.post("/game/{game_id}/move", response_model=GameStateModel)
def make_move(game_id: str, move: MoveModel, current_user: Optional[User] = Depends(get_current_user_optional)):
    print("move endpoint called with game_id:", game_id)
    print("games keys:", list(games.keys()))
    state = games.get(game_id)
    if not state:
        raise HTTPException(status_code=404, detail="Game not found")
    result, new_state = create.applyMove(state, move.dict())
    
    if not result.get('correct', False):
        raise HTTPException(status_code=400, detail=result.get('message', 'Invalid move'))
    
    games[game_id] = new_state

    if new_state.get("completed") and current_user:
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.username == current_user.username).first()
            if user and user.stats:
                stats = user.stats
                stats.games_played += 1
                stats.total_moves += len(new_state.get("steps", []))
                if new_state.get("won", True):
                    stats.games_won += 1
                    stats.current_win_streak += 1
                    if stats.current_win_streak > stats.longest_win_streak:
                        stats.longest_win_streak = stats.current_win_streak
                else:
                    stats.current_win_streak = 0
                if stats.games_played > 0:
                    stats.average_moves = stats.total_moves / stats.games_played
                time_taken = new_state.get("time", None)
                if time_taken is not None:
                    if stats.best_time is None or time_taken < stats.best_time:
                        stats.best_time = time_taken
                    prev_total_time = stats.average_time * (stats.games_played - 1)
                    stats.average_time = (prev_total_time + time_taken) / stats.games_played
                db.commit()
        finally:
            db.close()
    return GameStateModel(**new_state)

users = {}  

class UserRegisterModel(BaseModel):
    username: str
    password: str

@app.post("/user/register")
def register_user(user: UserRegisterModel):
    db = SessionLocal()
    try:
        hashed_password = get_password_hash(user.password)
        db_user = User(username=user.username, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        db_stats = UserStats(user_id=db_user.id)
        db.add(db_stats)
        db.commit()
        return {"message": "User registered successfully"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username already exists")
    finally:
        db.close()

@app.post("/game/{game_id}/reset", response_model=GameStateModel)
def reset_game(game_id: str):
    state = games.get(game_id)
    if not state:
        raise HTTPException(status_code=404, detail="Game not found")
    difficulty = state.get('difficulty', 1)
    new_state = create.createGame(difficulty=difficulty)
    games[game_id] = new_state
    return GameStateModel(**new_state)

@app.get("/stats")
def get_stats():
    total_games = len(games)
    completed_games = sum(1 for g in games.values() if g.get('completed'))
    avg_moves = (
        sum(len(g.get('steps', [])) for g in games.values()) / total_games
        if total_games else 0
    )
    return {
        "total_games": total_games,
        "completed_games": completed_games,
        "average_moves": avg_moves
    }


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

class Token(BaseModel):
    access_token: str
    token_type: str

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/user/login", response_model=Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()
    try:
        db_user = db.query(User).filter(User.username == form_data.username).first()
        if not db_user or not verify_password(form_data.password, db_user.hashed_password):
            raise HTTPException(status_code=401, detail="Incorrect username or password")
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": db_user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    finally:
        db.close()

@app.get("/user/stats")
def get_user_stats(current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    try:
        stats = db.query(UserStats).filter(UserStats.user_id == current_user.id).first()
        if not stats:
            raise HTTPException(status_code=404, detail="Stats not found")
        return {
            "games_played": stats.games_played,
            "games_won": stats.games_won,
            "average_moves": stats.average_moves,
            "best_time": stats.best_time,
            "average_time": stats.average_time,
            "longest_win_streak": stats.longest_win_streak,
            "current_win_streak": stats.current_win_streak,
            "total_moves": stats.total_moves
        }
    finally:
        db.close()
