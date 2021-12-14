from pydantic import BaseModel

class AuthToken(BaseModel):
	token : str

class Auth(BaseModel):
	username : str 
	password : str 

