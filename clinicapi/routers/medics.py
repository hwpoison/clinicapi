from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..dependencies import get_db, UserTokenAuth
from ..schemas import medics as schemes
from ..services.medics import Medics

router = APIRouter(
    prefix='/medics',
    tags=['Medicos'],
    dependencies=[Depends(UserTokenAuth())]
)


@router.get('/',
            response_model=List[schemes.MedicFullInfo],
            status_code=status.HTTP_200_OK)
def get_all_medics(
        db: Session = Depends(get_db)):
    return Medics(db).get_all()

@router.get('/{medic_id}',
            response_model=schemes.MedicInfo,
            status_code=status.HTTP_200_OK)
def get_medic(
        medic_id: int,
        db: Session = Depends(get_db)):
    medic = Medics(db).medic(medic_id)
    return medic

@router.get('/search/{string}',
            response_model=List[schemes.MedicFullInfo],
            status_code=status.HTTP_200_OK)
def patients_find(
        string: str,
        db: Session = Depends(get_db)):
    return Medics(db).search(string)


@router.post('/register',
             status_code=status.HTTP_201_CREATED)
def medic_register(
        info: schemes.MedicInfo,
        db: Session = Depends(get_db)):
    new_medic = Medics(db).register(info)
    return new_medic


@router.put('/{medic_id}',
            status_code=status.HTTP_202_ACCEPTED)
def medic_update(
        medic_id: int,
        info: schemes.MedicInfo,
        db: Session = Depends(get_db)):
    update_info = Medics(db).update_info(medic_id, info)
    return update_info


@router.delete('/{medic_id}',
               status_code=status.HTTP_200_OK)
def medic_delete(
        medic_id: int,
        db: Session = Depends(get_db)):
    return Medics(db).delete(medic_id)


@router.get('/{medic_id}/specialties',
            status_code=status.HTTP_200_OK)
def medic_delete(
        medic_id: int,
        db: Session = Depends(get_db)):
    return Medics(db).specialties(medic_id)
