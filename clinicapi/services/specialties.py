from dataclasses import dataclass

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from ..utils.ORM_utils import ORM
from ..models import clinica as models
from ..schemas import specialties as schemes
from ..utils.exception import Exceptional, ResponseInfo


@dataclass
class Specialties:
    db_session: Session
    validation_errors = {
        'not found':'Especialidad no encontrada',
        'already exists':'Esa especialidad ya existe.'
    }
    def specialty(self, id):
        specialty = self.get_by_id(id)
        if not specialty:
            raise Exceptional(validation_errors['not found'], 404)
        return specialty

    def get_all(self):
        return self.db_session.query(models.Especialidades).all()

    def add(self, info: schemes.SpecialtyBase):
        exists = self.get_by_name(info.nombre)
        if exists:
            raise Exceptional(validation_errors['not found'], 409)

        new_specialty = models.Especialidades(info.nombre, info.descripcion)
        if ORM(self.db_session).add(new_specialty):
            return ResponseInfo('Especialidad registrada correctamente.')

    def delete(self, id):
        specialty = self.get_by_id(id)
        if not specialty:
            raise Exceptional(validation_errors['not found'], 404)

        if ORM(self.db_session).delete(specialty):
            return ResponseInfo('Especialidad eliminada.')

        raise Exceptional('Problema al eliminar la especialidad.', 500)

    def search(self, string: str):
        result = self.db_session.query(models.Especialidades).filter(
            or_(
                models.Especialidades.nombre.like(f"%{string}%"),
                models.Especialidades.descripcion.like(f"%{string}%"))
            ).all()

        return result

    def get_by_id(self, id: int):
        return self.db_session.query(models.Especialidades).filter_by(id=id).first()

    def get_by_name(self, name: str):
        return self.db_session.query(models.Especialidades).filter_by(nombre=name).first()

    def update_info(self, id: int, info: schemes.SpecialtyBase):
        exists = self.get_by_id(id)
        if not exists:
            raise Exceptional(validation_errors['not found'], 404)

        new_info = exists
        new_info.nombre = info.nombre
        new_info.descripcion = info.descripcion

        if ORM(self.db_session).add(new_info):
            return ResponseInfo('Especialidad actualizada correctamente.')

        raise Exceptional('Problem al actualizar la especialidad.', 500)

    def practices(self, specialty_id): # add scheme for avoid asociation 
        return self.db_session.query(models.Practicas)\
        .join(models.Practicas.especialidad_r)\
        .where(models.Especialidades.id == specialty_id).all()

    def add_practice(self, info: schemes.Practice):
        specialty = self.get_by_id(info.especialidad_id)
        if not specialty:
            raise Exceptional(validation_errors['not found'], 404)

        new_practice = models.Practicas(
           especialidad=info.especialidad_id, desc=info.descripcion, costo=info.costo)
        
        if ORM(self.db_session).add(new_practice):
            return ResponseInfo('Practica registrada correctamente.')

        raise Exceptional('Problema al añadir la practica.', 500)

    def del_practice(self, practice_id: int):
        practice = self.db_session.query(models.Practicas).filter_by(id=practice_id).first()
        if not practice:
            raise Exceptional('La practica no se encuentra registrada.', 404)

        if ORM(self.db_session).delete(practice):
            return ResponseInfo('Practica eliminada.')

        raise Exceptional('Problema al eliminar la practica.', 500)

    def update_practice(self, practice_id : int, info: schemes.PracticeUpdate):
        practice = self.db_session.query(models.Practicas).filter_by(id=practice_id).first()
        if not practice:
            raise Exceptional('La practica no existe.', 404)

        new_info = practice 
        new_info.descripcion = info.descripcion 
        new_info.costo = info.costo 

        if ORM.add(self.db, new_info):
            return ResponseInfo('Practica actualizada correctamente.')

        raise Exceptional('Problem al actulizar la practica.', 500)
