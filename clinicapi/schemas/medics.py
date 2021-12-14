from pydantic import BaseModel
from typing import List

class MedicInfo(BaseModel):
	matricula : str 
	nombre : str
	apellido : str 
	domicilio : str 
	email : str 
	telefono : str 
	class Config:
		orm_mode = True

class MedicFullInfo(MedicInfo):
	id: int 
	class Config:
		orm_mode = True

class MedicList(BaseModel):
	medics : List[MedicFullInfo]
	class Config:
		orm_mode = True 