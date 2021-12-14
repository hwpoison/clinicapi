from dataclasses import dataclass

from sqlalchemy.orm import Session
from sqlalchemy import  or_, and_

from ..utils.ORM_utils import ORM
from ..models import clinica as models
from ..schemas import patients as patients_schemes
from ..utils.exception import Exceptional, ResponseInfo


@dataclass
class Patients:
    db_session : Session

    validation_errors = {
        'not found':"El paciente no se encuentra registrado.",
        'already exists':"El paciente ya se encuentra registrado."
    }

    def patient(self, id:int):
        patient = self.get_by_id(id)
        if not patient:
            raise Exceptional(self.validation_errors['not found'], 404)
        return patient

    def get_by_id(self, id: int):
        return self.db_session.query(models.Patients).filter_by(id=id).first()

    def get_by_dni(self, dni: int):
        return self.db_session.query(models.Patients).filter_by(dni=dni)

    def get_all(self):
        return self.db_session.query(models.Patients).all()

    def register(self, info: patients_schemes.PatientInfo):
        exists = self.get_by_dni(info.dni).first()
        if exists:
            raise Exceptional(self.validation_errors['already exists'], 409)
        new_patient = models.Patients(
            name=info.name, 
            lastname=info.lastname,
            address=info.address,
            phone=info.phone,
            observations=info.observations,
            dni=info.dni
        )
        if ORM(self.db_session).add(new_patient):
            return ResponseInfo("Paciente registrado con exito!")

        raise Exceptional('Problema al registrar el paciente.', 500)

    def update_info(self, id: int, info: patients_schemes.PatientInfo):
        exists = self.get_by_id(id)
        if not exists:
            raise Exceptional(self.validation_errors['not found'], 404)
        if (exists.dni != info.dni) and self.get_by_dni(info.dni).first():
            raise Exceptional('El DNI ya se encuentra registrado.', 409)

        new_info = exists
        new_info.name = info.name
        new_info.lastname = info.lastname 
        new_info.address = info.address 
        new_info.phone = info.phone
        new_info.observations = info.observations
        new_info.dni = info.dni

        if ORM(self.db_session).add(new_info):
            return ResponseInfo('Información actualizada')

        raise Exceptional('Problema al actulizar la información, por favor revise los campos.', 500)

    def delete(self, id):
        patient = self.db_session.query(models.Patients).filter_by(id=id).first()
        if not patient:
            raise Exceptional(self.validation_errors['not found'], 204)
        if ORM(self.db_session).delete(patient):
            return ResponseInfo('Paciente eliminado correctamente.')
        
        raise Exceptional('Problema al eliminar al paciente!', 500)

    def clinic_history(self, patient_id: int):
        if not self.get_by_id(patient_id):
            raise Exceptional(self.validation_errors['not found'], 404)
        history = self.db_session.query(models.ClinicalHistory).filter_by(patient=patient_id).first()
        if not history:
            raise Exceptional('El paciente no tiene historia clinica.', 404)
        return history

    def search(self, string: str):
        result = self.db_session.query(models.Patients).filter(
            or_(
                models.Patients.name.like(f"%{string}%"),
                models.Patients.lastname.like(f"%{string}%"),
                models.Patients.dni.like(f"%{string}%"),
                models.Patients.address.like(f"%{string}%"),
                models.Patients.phone.like(f"%{string}%"),
                models.Patients.observations.like(f"%{string}%"))
            ).all()

        return result