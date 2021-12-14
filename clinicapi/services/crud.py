import time
import logging
from datetime import datetime
from dataclasses import dataclass

from sqlalchemy.orm import Session
from sqlalchemy import  or_, and_

from ..models import clinica as models
from ..import schemes
from ..config.database import Base
from ..utils.ORM_utils import ORM
from ..schemas import patients as patients_schemes
from ..schemas import specialties as specialties_schemes
from ..utils.exception import Exceptional, ResponseInfo
