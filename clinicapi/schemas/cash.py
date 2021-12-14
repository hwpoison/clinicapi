from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from fastapi import Query 

class CashMovement(BaseModel):
	#codigo_movimiento : int 
	#fecha : datetime
	concept : str
	entry_money : float 
	out_money : float 
	user : int 
	invoice : int 
	sale_point : int
	class Config:
		orm_mode = True

class MovementSummary(BaseModel):
	id : int
	concept: str 
	entry_money: float 
	out_money : float 
	sale_point : int 
	name: str 
	description : str 

class MovementsSummary(BaseModel):
	movements : List[MovementSummary]
	class Config:
		orm_mode = True