from dataclasses import dataclass

from sqlalchemy.orm import Session
from sqlalchemy import  or_, and_

from ..utils.ORM_utils import ORM
from ..models import clinica as models
from ..schemas import patients as patients_schemes
from ..schemas import medics as medics_schemes
from ..utils.exception import Exceptional, ResponseInfo

@dataclass
class Medics:
    db_session : Session 

    validation_errors = {
        'not found':'El profesional no existe.'
    }
    def get_by_id(self, id: int):
        return self.db_session.query(models.Profesionales).filter_by(id=id).first()

    def get_by_matricula(self, matricula: int):
        return self.db_session.query(models.Profesionales).filter_by(matricula=matricula).first()

    def medic(self, id: int):
        medic = self.get_by_id(id)
        if not medic:
            raise Exceptional(validation_errors['not found'], 404)
        return medic 

    def get_all(self):
        print({'medics':self.db_session.query(models.Profesionales).all()})
        return self.db_session.query(models.Profesionales).all()

    def register(self, info: medics_schemes.MedicInfo):
        exists = self.get_by_matricula(info.matricula)
        if exists:
            raise Exceptional('El profesional ya se encuentra registrado.', 409)

        new_medic = models.Profesionales(
            nombre=info.nombre, 
            apellido=info.apellido,
            domicilio=info.domicilio,
            telefono=info.telefono,
            email=info.email,
            matricula=info.matricula
        )

        if ORM(self.db_session).add(new_medic):
            return ResponseInfo("Información registrada correctamente.")

        raise Exceptional('Problema al registrr al profesional.', 500)
    
    def update_info(self, id: int, info: patients_schemes.PatientInfo):
        exists = self.get_by_id(id)
        if not exists:
            raise Exceptional(validation_errors['not found'], 404)

        new_info = exists
        new_info.nombre = info.nombre
        new_info.apellido = info.apellido 
        new_info.domicilio = info.domicilio 
        new_info.telefono = info.telefono
        new_info.email = info.email
        new_info.matricula = info.matricula

        if ORM(self.db_session).add(new_info):
            return ResponseInfo('Información del profesional actulizada correctamente.')

        raise Exceptional('Problema al actualizar la información del profesional.', 500)
    
    def delete(self, id):
        medic = self.db_session.query(models.Profesionales).filter_by(id=id).first()
        if not medic:
            raise Exceptional(validation_errors['not found'], 204)

        if ORM(self.db_session).delete(medic):
            return ResponseInfo('Profesional eliminado.')
        
        raise Exceptional('Problema al eliminar al profesional.', 500)

    def specialties(self, medic_id):
        medic = self.get_by_id(medic_id)
        specialties = self.db_session.query(models.Especialidades).join(
            models.Especialistas.r_especialista, 
            models.Especialistas.r_especialidad).where(models.Profesionales.id==medic_id).all()
        return specialties

    def search(self, string: str):
        result = self.db_session.query(models.Profesionales).filter(
            or_(
                models.Profesionales.nombre.like(f"%{string}%"),
                models.Profesionales.apellido.like(f"%{string}%"),
                models.Profesionales.domicilio.like(f"%{string}%"),
                models.Profesionales.telefono.like(f"%{string}%"),
                models.Profesionales.matricula.like(f"%{string}%"))
            ).all()

        return result