from pydantic import BaseModel, Json
from datetime import datetime
from typing import Optional, List
from fastapi import Query 

class BaseInvoice(BaseModel):
	patient: int 
	total : float
	details : str # fix json validation

class InvoiceDetail(BaseModel):
	pass	

class Invoice(BaseModel):
	date : datetime
	patient : int 
	practices : List[str]
	total : float
	class Config:
		orm_mode = True 
