from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..services.specialties import Specialties
from ..schemas import specialties as schemes
from ..utils.exception import Exceptional
from ..dependencies import get_db, UserTokenAuth


router = APIRouter(
    prefix='/specialties',
    tags=['Especialidades'],
    dependencies=[Depends(UserTokenAuth())]
)


@router.get('/',
            response_model=List[schemes.SpecialtyInfo],
            status_code=status.HTTP_200_OK)
def get_all_specialties(db: Session = Depends(get_db)):
    return Specialties(db).get_all()

@router.get('/search/{string}',
            response_model=List[schemes.SpecialtyInfo],
            status_code=status.HTTP_200_OK)
def specialty_find(
        string: str,
        db: Session = Depends(get_db)):
    return Specialties(db).search(string)


@router.get('/{specialty_id}',
            response_model=schemes.SpecialtyBase,
            status_code=status.HTTP_200_OK)
def get_specialty(
        specialty_id: int,
        db: Session = Depends(get_db)):
    medic = Specialties(db).specialty(specialty_id)
    return medic


@router.post('/register',
             status_code=status.HTTP_201_CREATED)
def specialty_add(
        info: schemes.SpecialtyBase,
        db: Session = Depends(get_db)):
    new_medic = Specialties(db).add(info)
    return new_medic


@router.put('/{specialty_id}',
            status_code=status.HTTP_202_ACCEPTED)
def specialty_update(
        specialty_id: int,
        info: schemes.SpecialtyBase,
        db: Session = Depends(get_db)):
    update_info = Specialties(db).update_info(specialty_id, info)
    return update_info


@router.delete('/{specialty_id}',
           status_code=status.HTTP_200_OK)
def specialty_delete(
        specialty_id: int,
        db: Session = Depends(get_db)):
    return Specialties(db).delete(specialty_id)


@router.get('/{specialty_id}/practices',
            status_code=status.HTTP_200_OK)
def specialty_practice(
        specialty_id: int,
        db: Session = Depends(get_db)):
    return Specialties(db).practices(specialty_id)


@router.post('/{specialty_id}/practices/',
            status_code=status.HTTP_200_OK)
def specialty_practice(
        info : schemes.Practice,
        db: Session = Depends(get_db)):
        return Specialties(db).add_practice(info)

@router.delete('/{specialty_id}/practices/{practice_id}',
            status_code=status.HTTP_200_OK)
def specialty_practice(
        practice_id : int,
        db: Session = Depends(get_db)):
        return Specialties(db).del_practice(practice_id)

@router.put('/{specialty_id}/practices/{practice_id}',
            status_code=status.HTTP_202_ACCEPTED)
def specialty_update(
        practice_id : int,
        info: schemes.PracticeUpdate,
        db: Session = Depends(get_db)):
    update_info = Specialties(db).update_practice(practice_id, info)
    return update_info

