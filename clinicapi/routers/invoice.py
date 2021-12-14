from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..dependencies import get_db, UserTokenAuth
#schemes
from ..services.invoice import Invoice
from ..schemas import invoices as schemes

router = APIRouter(
    prefix='/invoices',
    tags=['Facturación'],
    #dependencies=[Depends(auth.current_user)],
    responses={404: {"description": "Not found"}}
)

@router.get('/', 
       response_model= List[schemes.Invoice],
        status_code=status.HTTP_200_OK)
def get_all_invoices(
    db: Session = Depends(get_db)):
    print("Getting invoices")
    return Invoice(db).get_all()

# Creacion de factura, agregar sistema de codigo y cosas de facturas electronicas.
@router.post('/',
        status_code=status.HTTP_201_CREATED)
def create(info : schemes.Invoice, db: Session = Depends(get_db)):
    return Invoice(db).create(info)