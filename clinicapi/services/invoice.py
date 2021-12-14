from dataclasses import dataclass

from sqlalchemy.orm import Session
from sqlalchemy import  or_, and_

from ..schemas import invoices as schemes
from ..utils.ORM_utils import ORM
from ..models import clinica as models
from ..utils.exception import Exceptional

@dataclass
class Invoice:
	db: Session 

	def get_all(self):
		return self.db.query(models.Invoice).all()

	def create(self, info: schemes.BaseInvoice):
		new_invoice = models.Planillas(
			total=info.total,
			paciente=info.paciente 
		)
		print("Crear factura o planilla:", new_invoice)
		print(">>>", info.details)