from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from ..utils.exception import Exceptional
from ..utils.pdf_generator.ticket_generator import invoice


router = APIRouter(
    prefix='/tickets',
    tags=['Emisión de tickets'],
    dependencies=[],
)

@router.get('/invoice')
async def gen(motivo: str):
    print(motivo)
    pdf_path = invoice({'fecha': "2021", 'motivo': motivo})
    return FileResponse(path=pdf_path,
        headers={'Content-Disposition':f'inline;filename="{pdf_path.stem}.pdf"'},
        media_type='application/pdf')