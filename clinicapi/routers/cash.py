from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_db, UserTokenAuth
from ..schemas import cash as schemes
from ..utils.exception import Exceptional
from ..services.cash import Cash

router = APIRouter(
    prefix='/cash',
    tags=['Caja'],
    dependencies=[Depends(UserTokenAuth())]
)

@router.get('/',
         response_model=schemes.MovementsSummary,
         status_code=status.HTTP_200_OK)
def all_movements(
        db: Session = Depends(get_db)):
    return Cash(db).get()


@router.post('/add')
def new_movement(
        info: schemes.CashMovement,
        db: Session = Depends(get_db)):
    return Cash(db).add(info)




# CONSULTAS


"""
#@app.post('/cash/movements/add')
    + id 
    + fecha (timestamp)
    + concepto
    + ingreso
    + egreso 
    + usuario
    + codigo de caja 


#@app.post('/cash/move/list')

"""
