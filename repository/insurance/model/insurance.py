from config.database import Base
from sqlalchemy import Column, DECIMAL, Integer, String, Boolean,DateTime, Enum as sqlEnum, ForeignKey
from enum import Enum
from datetime import datetime

class Role(Enum):
      ROLE_ADMIN = 'ROLE_ADMIN'
      ROLE_CUSTOMER = 'ROLE_CUSTOMER'
      ROLE_AGENT = 'ROLE_AGENT'

class InsuranceType(Enum):
     LIFE = 'LIFE'
     CHILD = 'CHILD'
     RETIREMENT = 'RETIREMENT'
     SAVINGS = 'SAVINGS'
     INVESTMENT = 'INVESTMENT'

class InterestType(Enum):
     SIMPLE = 'SIMPLE'
     COMPOUND = 'COMPOUND'

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key= True, autoincrement= 'auto', index = True)
    firstname = Column(String, nullable = False)
    lastname = Column(String, nullable = False)
    email = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False)
    role = Column(sqlEnum(Role), default = Role.ROLE_ADMIN, nullable = False)
    created_at = Column(DateTime(), default = datetime.now())
    updated_at = Column(DateTime(), onupdate = datetime.now(), default = datetime.now())

    def __init__(self, email, firstname, lastname, password, role, id = None):
        self.id = id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
        self.role = role


class InsurancePlan(Base):
    __tablename__ = 'insurance_plan'
    id = Column(Integer, primary_key= True, autoincrement= 'auto', index = True)
    insurance_name = Column(String, nullable = False, unique=True)
    description = Column(String, nullable=False)
    insurance_type = Column(sqlEnum(InsuranceType), nullable = False)
    created_at = Column(DateTime(), default = datetime.now())
    updated_at = Column(DateTime(), onupdate = datetime.now(), default = datetime.now())  

    def __init__(self, insurance_name, description, insurance_type, id = None):
         self.insurance_name = insurance_name
         self.id = id 
         self.description = description
         self.insurance_type = insurance_type


class LifeInsuranceDetail(Base):
    __tablename__ = 'life_insurance_details'
    id = Column(Integer, primary_key= True, autoincrement= 'auto', index = True)
    insurance_id = Column(Integer, ForeignKey("insurance_plan.id"), nullable = False)
    plan_code = Column(String, unique=True, nullable = False)
    basic_sum_assured = Column(Integer, nullable = False)
    duration = Column(Integer, nullable=False)
    interest = Column(DECIMAL, nullable=False)
    interest_type = Column(sqlEnum(InterestType, nullable = False))
    is_deleted = Column(Boolean, default = False) 
    created_at = Column(DateTime(), default = datetime.now())
    updated_at = Column(DateTime(), onupdate = datetime.now(), default = datetime.now())  

    def __init__(self, insurance_id, plan_code, basic_sum_assured, duration, interest, interest_type, id = None):
         self.id = id 
         self.insurance_id = insurance_id
         self.plan_code = plan_code
         self.basic_sum_assured = basic_sum_assured
         self.duration = duration
         self.interest = interest
         self.interest_type = interest_type