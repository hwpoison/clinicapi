from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..dependencies import get_db, UserTokenAuth
from ..schemas import patients as schemes
from ..services.patients import Patients

router = APIRouter(
    prefix='/patients',
    tags=['Pacientes'],
    dependencies=[Depends(UserTokenAuth())],
    responses={404: {"description": "Not found"}}
)

@router.get('/', 
        response_model= List[schemes.PatientFullInfo],
        status_code= status.HTTP_200_OK)
async def all_patients(
    db: Session = Depends(get_db)):
    return Patients(db).get_all()

@router.get('/{patient_id}',
        response_model=schemes.PatientInfo,
        status_code=status.HTTP_200_OK)
async def get_patient(
    patient_id: int, 
    db: Session = Depends(get_db)):
    patient = Patients(db).patient(patient_id)
    return patient

@router.get('/search/{string}', 
        response_model= List[schemes.PatientFullInfo],
        status_code=status.HTTP_200_OK)
async def find_patient(string: str, db: Session = Depends(get_db)):
    return Patients(db).search(string)

@router.post('/register',
    status_code=status.HTTP_201_CREATED)
async def patient_register(info: schemes.PatientInfo, db: Session = Depends(get_db)):
    new_patient = Patients(db).register(info)
    return new_patient

@router.put('/{patient_id}',
        status_code=status.HTTP_202_ACCEPTED)
async def update_patient_info(
    patient_id: int, 
    info: schemes.PatientInfo, 
    db: Session = Depends(get_db)):
    update_info = Patients(db).update_info(patient_id, info)
    return update_info

@router.delete('/{patient_id}',
        status_code=status.HTTP_200_OK)
async def delete_patient(patient_id: int,
    db: Session = Depends(get_db)):
    return Patients(db).delete(patient_id)

@router.get('/{patient_id}/history',
        response_model=schemes.PatientHistory,
        status_code=status.HTTP_200_OK)
async def get_patient_historial(patient_id: int, db: Session = Depends(get_db)):
    return Patients(db).clinic_history(patient_id)

