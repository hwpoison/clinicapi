from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from fastapi import Query 

class SpecialtyBase(BaseModel):
	nombre : str 
	descripcion : str 
	class Config:
		orm_mode = True 

class SpecialtyInfo(SpecialtyBase):
	id : int 
	class Config:
		orm_mode = True

class SpecialtyList(BaseModel):
	specialties: List[SpecialtyInfo]
	class Config:
		orm_mode = True

class Practice(BaseModel):
	especialidad_id : int
	costo : float
	descripcion: str

class PracticeUpdate(BaseModel):
	descripcion : str 
	costo : float