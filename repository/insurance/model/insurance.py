from config.database import Base
from sqlalchemy import Column, Integer, String, Float, Boolean,DateTime, Enum as sqlEnum, ForeignKey
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

class Healthy(Enum):
     EXCELLENT = 'EXCELLENT'
     GOOD = 'GOOD'
     FAIR = 'FAIR'
     POOR = 'POOR'

class LifeStyle(Enum):
     SEDENTARY = 'SEDENTARY'
     ACTIVE = 'ACTIVE'
     MODERATELY_ACTIVE = 'MODERATELY_ACTIVE'

class OccupationType(Enum):
     HIGH_RISK = 'HIGH_RISK'
     MEDIUM_RISK = 'MEDIUM_RISK' 
     LOW_RISK = 'LOW_RISK'

class PaymentStatus(Enum):
     NOT_PAID = 'NOT_PAID'
     PAID = 'PAID'

class OrderStatus(Enum):
     UNDER_REVIEW = 'UNDER_REVIEW'
     PENDING = 'PENDING' 
     PAYMENT_FAILED = 'PAYMENT_FAILED'
     CONFIRMED = 'CONFIRMED' 
     CANCELLED = 'CANCELLED'

class PremiumType(Enum):
     MONTHLY  = 'MONTHLY' 
     QUARTERLY = 'QUARTERLY' 
     HALF_YEARLY = 'HALF_YEARLY' 
     ANNUAL = 'ANNUAL'

class TaskStatus(Enum):
     INITIALISED = 'INITIALISED' 
     DELAYED = 'DELAYED' 
     DELAYED_PAYMENT = 'DELAYED_PAYMENT' 
     AWAITING_PAYMENT = 'AWAITING_PAYMENT' 
     INFORCE = 'INFORCE'

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
    interest = Column(Float, nullable=False)
    interest_type = Column(sqlEnum(InterestType), nullable = False)
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



class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key= True, autoincrement= 'auto', index = True)
    firstname = Column(String, nullable = False)
    lastname = Column(String, nullable = False)
    healthy = Column(sqlEnum(Healthy), nullable = False)
    life_style = Column(sqlEnum(LifeStyle), nullable = False)
    occupation = Column(String, nullable=False)
    occupation_type = Column(sqlEnum(OccupationType), nullable = False)
    city = Column(String, nullable=False)
    pincode = Column(String, nullable=False)
    lat = Column(String, nullable=False)
    lng = Column(String, nullable=False)
    first_line = Column(String, nullable=False)
    last_line = Column(String)
    land_mark = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=False, unique=True)
    is_deleted = Column(Boolean, default = False)
    created_at = Column(DateTime(), default = datetime.now())
    updated_at = Column(DateTime(), onupdate = datetime.now(), default = datetime.now())

    def __init__(self, firstname, lastname, healthy, life_style, occupation, occupation_type, city, pincode, lat, lng, first_line, last_line, land_mark, email, phone, id = None):
         self.id = id
         self.firstname = firstname
         self.lastname = lastname
         self.healthy = healthy
         self.life_style = life_style
         self.occupation = occupation
         self.occupation_type = occupation_type
         self.city = city
         self.pincode = pincode
         self.lat = lat
         self.lng = lng
         self.first_line = first_line
         self.last_line = last_line
         self.land_mark = land_mark
         self.email = email
         self.phone = phone


class Agent(Base):
    __tablename__ = 'agents'
    id = Column(Integer, primary_key= True, autoincrement= 'auto', index = True)
    firstname = Column(String, nullable = False)
    lastname = Column(String, nullable = False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime(), default = datetime.now())
    updated_at = Column(DateTime(), onupdate = datetime.now(), default = datetime.now())

    def __init__(self, firstname, lastname, email, phone, id = None):
         self.id = id
         self.firstname = firstname
         self.lastname = lastname
         self.email = email
         self.phone = phone



class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key= True, autoincrement= 'auto', index = True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable = False)
    insurance_id = Column(Integer, ForeignKey("insurance_plan.id"), nullable = False)
    sub_insurance_id = Column(Integer, nullable=False)
    amount_to_pay = Column(Float, nullable = False)
    amount_paid = Column(Float, nullable = False, default=0)
    order_status = Column(sqlEnum(OrderStatus), nullable = False) 
    payment_status = Column(sqlEnum(PaymentStatus), nullable=False, default=PaymentStatus.NOT_PAID)
    premium_type = Column(sqlEnum(PremiumType), nullable = False)
    created_by  = Column(Integer, ForeignKey("users.id"), nullable = False)
    approved_by  = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(), default = datetime.now())
    updated_at = Column(DateTime(), onupdate = datetime.now(), default = datetime.now())

    def __init__(self, customer_id, insurance_id, amount_to_pay, order_status, created_by, premium_type, approved_by = None, id = None, sub_insurance_id = None, amount_paid = 0, payment_status = PaymentStatus.NOT_PAID):
         self.id = id
         self.customer_id = customer_id
         self.insurance_id = insurance_id
         self.sub_insurance_id = sub_insurance_id
         self.amount_to_pay = amount_to_pay
         self.amount_paid = amount_paid
         self.order_status = order_status
         self.payment_status = payment_status
         self.premium_type = premium_type
         self.created_by = created_by
         self.approved_by = approved_by



class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key= True, autoincrement= 'auto', index = True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable = False)
    premium_amount_to_pay = Column(Float, nullable = False)
    premium_amount_paid = Column(Float, nullable = False, default=0)
    premium_type = Column(sqlEnum(PremiumType), nullable = False)
    premium_penalty = Column(Float, nullable = False, default=0)
    task_status = Column(sqlEnum(TaskStatus), nullable=False) 
    payment_status = Column(sqlEnum(PaymentStatus), nullable=False)
    paid_at = Column(DateTime())
    created_at = Column(DateTime(), default = datetime.now())
    updated_at = Column(DateTime(), onupdate = datetime.now(), default = datetime.now())

    def __init__(self, order_id, premium_amount_to_pay, premium_type, task_status, payment_status, paid_at = None, premium_penalty = 0, premium_amount_paid = 0, id = None):
         self.id = id
         self.order_id = order_id
         self.premium_amount_to_pay = premium_amount_to_pay
         self.premium_amount_paid = premium_amount_paid
         self.premium_type = premium_type
         self.premium_penalty = premium_penalty
         self.task_status = task_status
         self.payment_status = payment_status
         self.paid_at = paid_at 