from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from ..schemas import auth as schemes
from ..utils.exception import Exceptional
from ..dependencies import get_db, UserTokenAuth

from ..services import auth

router = APIRouter(
    prefix='/auth',
    tags=['Autenticación'],
    dependencies=[],
)

@router.post("/login")
def generate_token(
    form_data: schemes.Auth,
    db: Session = Depends(get_db)):
    user = auth.Users(db).authenticate_user(form_data.username, form_data.password)
    return auth.Users.create_token(user)