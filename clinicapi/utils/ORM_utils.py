import logging

from sqlalchemy.orm import Session
from ..config.database import Base
from dataclasses import dataclass

@dataclass
class ORM:
    """ ORM utils for basic crud operations """
    db_session : Session

    def add(self, entity: Base):
        try:
            self.db_session.add(entity)
            self.db_session.commit()
            logging.info(f'[+]{entity} added and commited.')
            return True
        except Exception as err:
            self.db_session.rollback()
            logging.error(f'[x]{entity} add and commit error.')
            print(err.orig)
            return False

    def delete(self, entity: Base):
        try:
            self.db_session.delete(entity)
            self.db_session.commit()
            logging.info(f'[+]{entity} deleted and commited.')
            return True
        except Exception as err:
            self.db_session.rollback()
            logging.error(f'[x]{entity} deleted and commit error.')
            print(err.orig)
            return False

    def commit(self, entity: Base):
        try:
            self.db_session.commit()
            return True
        except IntegrityError as err:
            print(err)
            return False
