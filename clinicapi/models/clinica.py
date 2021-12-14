from datetime import datetime

from sqlalchemy.types import TIMESTAMP
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime,Time

from ..config.database import Base

class Invoice(Base):
    __tablename__ = 'invoices'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    date = Column(TIMESTAMP, nullable=False)
    patient = Column(Integer, ForeignKey('patients.id'))
    total= Column(Float)
    paid_out = Column(Float)

    def __init__(self, paciente, total, paid_out):
        self.date = datetime.now()
        self.patient = paciente 
        self.total = total 
        self.paid_out = paid_out

class InvoiceDetail(Base):
    __tablename__ = 'invoice_details'

    id = Column(Integer, primary_key=True)
    invoice = Column(Integer, ForeignKey('invoices.id'), nullable=False)
    practice = Column(Integer, ForeignKey('practices.id'), nullable=False)

    r_practice = relationship('Practices')
    r_invoice = relationship('Invoice')

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    username = Column(String(15), nullable=False, unique=True)
    password_hash = Column(String(256), nullable=False)
    email = Column(String(20), nullable=False)
    privileges = Column(Integer)

    def __init__(self, username, password_hash, email):
        self.username = username 
        self.email = email
        self.password_hash = password_hash
        self.privileges = 0

class Patients(Base):
    __tablename__ = 'patients'

    id =            Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    name =        Column(String(45), nullable=False)
    lastname =      Column(String(45), nullable=False)
    address =     Column(String(45))
    phone =      Column(String(45))
    observations =Column(String(50))
    dni =           Column(String(8) , unique=True)

    def __init__(self, name, lastname, address, phone, observations, dni):
        self.name = name
        self.lastname = lastname
        self.address = address 
        self.phone = phone 
        self.observations = observations 
        self.dni = dni

class SPOpenings(Base):
    __tablename__ = 'sp_openings'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    date =  Column(TIMESTAMP, nullable=False)
    sale_point = Column(Integer, ForeignKey('sales_point.id'), nullable=False)
    total_money = Column(Float, nullable=False)
    user = Column(Integer, ForeignKey('users.id'), nullable=False)

    user_r = relationship(Users, backref=backref('openings', uselist=True))

    def __init__(self, user, sale_point, total_money):
        self.user = user 
        self.sale_point = sale_point
        self.fecha = datetime.now()
        self.total_money = total_money

class SPCloses(Base):
    __tablename__ = 'sp_closes'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    date = Column(TIMESTAMP, nullable=False)
    sale_point = Column(Integer, ForeignKey('sales_point.id'), nullable=False)
    total_money = Column(Integer, nullable=False)
    user = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    def __init__(self, user, codigo_caja, total_money):
        self.user= user
        self.sale_point = codigo_caja
        self.date = datetime.now()
        self.total_money = total_money

class ClinicalHistory(Base):
    __tablename__ = 'clinical_histories'

    id = Column(Integer, nullable=False, primary_key=True)
    patient = Column(Integer, ForeignKey('patients.id'), unique=True, nullable=False)
    summary = Column(String(1000))

    patient_r = relationship('Patients')

class CashMovement(Base):
    __tablename__ = 'cash_movement'

    id = Column(Integer, primary_key=True, nullable=True, autoincrement=True)
    date = Column(DateTime, nullable=True)
    concept = Column(String, nullable=False)
    entry_money  = Column(Float, nullable=False)
    out_money = Column(Float, nullable=False)
    user  = Column(Integer, ForeignKey('users.id'), nullable=False)
    sale_point = Column(Integer, ForeignKey('sales_point.id'), nullable=False)

    def __init__(self, concept, entry_money, out_money, user, sale_point):
        self.concept = concept 
        self.entry_money = entry_money
        self.out_money =out_money 
        self.user = user 
        self.sale_point = sale_point

    user_r = relationship('Users')
    salepoint_r = relationship('SalesPoint')

class SalesPoint(Base):
    __tablename__ = 'sales_point'

    id = Column(Integer, primary_key=True)
    description = Column(String(100))

    def __init__(self, description):
        self.description = descripcion

class Specialists(Base):
    __tablename__ = 'specialists'

    id = Column(Integer, primary_key=True, nullable=True, autoincrement=True)
    medic = Column(Integer, ForeignKey('medics.id'))
    specialty = Column(Integer, ForeignKey('specialties.id'))

    medics_r = relationship('Medics')
    specialties_r = relationship('Specialties')

class Specialties(Base):
    __tablename__ = 'specialties'

    id = Column(Integer, primary_key=True, nullable=True, autoincrement=True)
    name = Column(String(45))
    description = Column(String(200))

    def __init__(self, name, description):
        self.name = name
        self.description = description

class Consultations(Base):
    __tablename__ = 'consultations'

    id = Column(Integer, primary_key=True, nullable=False)
    patient = Column(Integer, ForeignKey('patients.id'), unique=True, nullable=False)
    medic = Column(Integer, ForeignKey('medics.id'), nullable=False)
    date = Column(DateTime)
    reason = Column(String(150))
    practice = Column(Integer, ForeignKey('practices.id'), nullable=False)

class Medics(Base):
    __tablename__ = 'medics'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    registration = Column(Integer, nullable=False)
    name = Column(String(15), nullable=False)
    lastname = Column(String(15), nullable=False)
    address = Column(String(40))
    email = Column(String(30))
    phone = Column(String(15))

    def __init__(self, name, lastname, address, email, phone, registration):
        self.name = name 
        self.lastname = lastname 
        self.address = address 
        self.email = email 
        self.phone = phone 
        self.registration = registration

class Vouchers(Base):
    __tablename__ = 'vouchers'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    medic = Column(Integer, ForeignKey('medics.id'), nullable=False)
    patient = Column(Integer, ForeignKey('patients.id'))
    practice = Column(Integer, ForeignKey('practices.id'), nullable=True)
    description = Column(String(200))
    issue_date = Column(TIMESTAMP, nullable=False)
    hash = Column(String(128), nullable=False, unique=True)

    medics_r = relationship('Medics')
    patients_r = relationship('Patients')
    practices_r = relationship('Practices')

    def __init__(self, medic, patients, practice, description=""):
        self.medic = medic 
        self.patients = patients 
        self.fecha_emision = datetime.now()
        self.practice = practice
        self.description = description
        self.hash = self.dump_hash()

    def dump_hash(self): # separar responsabilidad
        hash = sha3_224()
        string = self.fecha_emision.strftime("%D %c")
        hash.update(bytearray(map(ord, string)))
        return hash.hexdigest()

class Practices(Base):
    __tablename__ = 'practices'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    specialty = Column(Integer, ForeignKey('specialties.id'), nullable=False)
    description = Column(String(300), nullable=True)
    price = Column(Float, nullable=True)

    def __init__(self,specialty, desc, costo):
        self.specialty = specialty 
        self.description = desc 
        self.price = price 

    specialties_r = relationship('Specialties')