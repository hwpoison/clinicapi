import logging
from ..utils.exception import Exceptional

from configparser import ConfigParser

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker

# read config file
config_file = ConfigParser()
config_file.read('clinicapi/config/db.conf')

# craft datbase url 
db_info = config_file['DB']
DB_URL = f"mysql://{ db_info['user'] }:{db_info['password'] }@localhost/{db_info['database']}?charset=utf8mb4"


engine = create_engine(DB_URL)  
db_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()