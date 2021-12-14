from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from fastapi import Query 

# User Schemes
user_length = Query(None, min_length=5, max_length=15)
password_length = Query(None, min_length=8, max_length=100)

class UserBase(BaseModel):
	username : str 
	email : str
	class Config:
		orm_mode = True 

class UserCreation(UserBase):
	password : str
	class Config:
		orm_mode = True 

class UserTokenContent(BaseModel):
	id : int 
	username : str
	class Config:
		orm_mode = True

class UserNewPassword(UserBase):
	username : str 
	old_password : str
	new_password : str
