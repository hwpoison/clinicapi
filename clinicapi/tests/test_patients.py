from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from ..main import app
from ..dependencies import UserTokenAuth
import os 

# TODO: implement dependency override with a class
os.environ['test_mode'] = 'yes' # bypass token auth

#app.dependency_overrides[UserTokenAuth] = lambda : 'test-case'

client = TestClient(app)


async def test_patients():
	all_patients = client.get('/patients')
	assert all_patients.status_code == 200