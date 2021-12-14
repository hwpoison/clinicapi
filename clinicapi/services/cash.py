from dataclasses import dataclass
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import  or_, and_

from ..utils.ORM_utils import ORM
from ..models import clinica as models
from ..schemas import cash as schemes
from ..utils.exception import Exceptional, ResponseInfo

@dataclass
class Cash:
    db : Session 

    def add(self, info: schemes.CashMovement):
        new_movement = models.CashMovement(
            concept=info.concept,
            entry_money=info.entry_money,
            out_money=info.out_money,
            user=info.user,
            sale_point=info.sale_point
        )
        new_movement.date = datetime.now()

        if ORM.add(self.db, new_movement):
            return ResponseInfo("Listo!")
        
        raise Exceptional("Problema", 500)

    def get(self):
        movement = self.db\
        .query(
            models.CashMovement.id,
            models.CashMovement.date,
            models.CashMovement.concept,
            models.CashMovement.entry_money,
            models.CashMovement.out_money,
            models.CashMovement.sale_point,
            models.User.username,
            models.SalesPoint.description)\
        .join(models.CashMovement.user_r,\
            models.CashMovement.sale_point)\
        .all()

        return {'movements':movement}