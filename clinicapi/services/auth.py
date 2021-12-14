import jwt
import logging
import datetime
from hashlib import sha256
from dataclasses import dataclass

from sqlalchemy.orm import Session
from fastapi import security, Depends, Header

from ..utils.exception import Exceptional, ResponseInfo
from ..models import clinica as models
from ..schemas import users as schemes
from ..dependencies import get_db, JWT_SECRET_KEY
from ..utils.ORM_utils import ORM

@dataclass
class Users:
    db_session: Session

    def register_user(self, info: schemes.UserCreation):
        # check if exists
        exists = self.get_by_name(info.username)
        if exists:
            raise Exceptional("El nombre de usuario está ocupado.", 409)
        if len(info.password) < 8:
            raise Exceptional('Contraseña demasiado corta',
                              406)  # todo: password validation

        # create new
        new_user = models.Users(
            username=info.username,
            password_hash=self.hash_plain_password(info.password),
            email=info.email
        )

        if ORM(self.db_session).add(new_user):
            return ResponseInfo("Usuario correctamente creado.")

        raise Exceptional('Problema al registrar el usuario.', 500)

    def authenticate_user(self, username: str, password: str):
        user = self.get_by_name(username)

        if not user or not self.verify_password(password, user.password_hash):
            raise Exceptional('Usuario o clave invalido.', 403)

        return user

    def create_token(user: models.Users):
        user_dict = schemes.UserTokenContent.from_orm(user)
        new_token = jwt.encode(user_dict.dict(), JWT_SECRET_KEY)

        return dict(access_token=new_token, token_type="bearer")

    def get_by_id(self, id: int):
        return self.db_session.query(models.Users).filter_by(id=id).first()

    def get_by_name(self, username: str):
        return self.db_session.query(models.Users)\
            .filter_by(username=username).first()

    def delete(self, id: int):
        user = self.db_session.query(models.Users).filter_by(id=id).username()
        if not user:
            raise Exceptional('Usuario no encontrado.', 404)
        if ORM(self.db_session).delete(user):
            return ResponseInfo('Usuario eliminado.')

        raise Exceptional('Problem to delete user', 500)

    def change_password(self, info: schemes.UserNewPassword):
        user = self.db_session.query(models.Users).filter_by(
            username=info.nombre).first()
        if not user:
            raise Exceptional('Usuario no encontrado!', 409)

        if len(info.new_password) < 8 or len(info.old_password) < 8:
            raise Exceptional('Contraseña demasiado corta.', 406)

        if self.verify_password(info.old_password, user.password_hash):
            new_password = self.hash_plain_password(info.new_password)
            user.password_hash = new_password
            if ORM(self.db_session).commit(user):
                return ResponseInfo('Contraseña cambiada correctamente.')
            else:
                raise Exceptional('Problema al cambiar la contraseña.', 409)

        raise Exceptional('La contraseña anterior parece ser incorrecta.', 409)

    def hash_plain_password(self, plain_password : str):
        b_hash = bytearray()
        b_hash.extend(map(ord, plain_password))
        return sha256(b_hash).hexdigest()

    def verify_password(self, password: str, hashed_password: str):
        return self.hash_plain_password(password) == hashed_password
