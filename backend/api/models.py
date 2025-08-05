from pydantic import BaseModel
from typing import Any, Optional

class MoveModel(BaseModel):
    num1: int
    num2: int
    operation: str

class GameStateModel(BaseModel):
    numbers: list[int]         
    target: int                
    steps: list[str]           
    completed: bool            
    message: Optional[str] = None  
    game_id: Optional[str] = None 

class ResultModel(BaseModel):
    correct: bool             
    message: str              
    new_state: GameStateModel  

class UserRegisterModel(BaseModel):
    username: str
    password: str
