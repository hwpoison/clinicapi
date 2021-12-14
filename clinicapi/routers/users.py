from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_db, UserTokenAuth
from ..schemas import users as schemes
from ..utils.exception import Exceptional

from ..services import auth

router = APIRouter(
    prefix='/users',
    tags=['Usuarios'],
    dependencies=[],
    #responses={404: {'description': 'User not found.'}}
)


@router.post('/register',
             status_code=status.HTTP_201_CREATED)
def create_user(
        info: schemes.UserCreation,
        db: Session = Depends(get_db)):
    user_creation = auth.Users(db).register_user(info)
    return user_creation


@router.get('/{user_id}',
            response_model=schemes.UserBase,
            status_code=status.HTTP_200_OK)
def get_user(
        user_id: int,
        db: Session = Depends(get_db)):
    user = auth.Users(db).get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail='user not found')
    return user


@router.put('/{user_id}/password',
            status_code=status.HTTP_200_OK)
def change_password(
        info: schemes.UserNewPassword,
        db: Session = Depends(get_db)):
    password_update = auth.Users(db).change_password(info)
    return password_update


@router.delete('/{user_id}/delete',
               status_code=status.HTTP_200_OK)
def user_delete(
        id: int,
        db: Session = Depends(get_db)):
    return auth.Users(db).delete(id)
