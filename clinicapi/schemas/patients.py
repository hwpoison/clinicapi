from pydantic import BaseModel, constr, validator
from datetime import datetime
from typing import Optional, List
from fastapi import Query 

dni = Query(None, min_length=5, max_length=15)

### Patient
class PatientInfo(BaseModel):
	name : str
	lastname : str
	address: str
	phone : str 
	observations : str 
	dni : constr(min_length=8, max_length=8)
	class Config:
		orm_mode = True

class PatientFullInfo(PatientInfo):
	id : int
	class Config:
		orm_mode = True

class PatientList(BaseModel):
	patients : List[PatientFullInfo]
	class Config:
		orm_mode = True

class PatientHistory(BaseModel):
	id : int 
	summary : str 
	class Config:
		orm_mode = True
