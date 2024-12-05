from config.database import Base
from sqlalchemy import Column, Integer, String, Boolean,DateTime, Enum as sqlEnum, ForeignKey
from enum import Enum
from datetime import datetime

class Role(Enum):
      ROLE_ADMIN = 'ROLE_ADMIN'
      ROLE_HR = 'ROLE_HR'
      ROLE_FINANCE = 'ROLE_FINANCE'
      ROLE_EMPLOYEE = 'ROLE_EMPLOYEE'

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
         

  

class Department(Base, object):
    __tablename__ = 'department'

    id = Column(Integer, primary_key = True, autoincrement='auto', index = True)
    name = Column(String, nullable= False)
    description = Column(String, nullable=False)
    is_approved = Column(Boolean, default = False)
    approved_by = Column(Integer)
    approved_at = Column(DateTime())
    deleted_by = Column(Integer)
    deleted_at = Column(DateTime())
    created_by = Column(Integer, nullable = False)
    is_deleted = Column(Boolean, default = False)
    created_at = Column(DateTime(), default = datetime.now())
    updated_at = Column(DateTime(), onupdate = datetime.now(), default = datetime.now())

    def __init__(self, name = None, description = None, created_by = None, id = None):
        self.id = id
        self.name = name 
        self.description = description
        self.created_by = created_by

    def json_serializer(obj):
        if isinstance(obj, Department):
           return {'id' : obj.id, 'name' : obj.name, 'description':obj.description, 'is_approved': obj.is_approved, 'is_deleted' : obj.is_deleted}
        raise TypeError('Object of type `Department` is not JSON serializable')


class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key = True, autoincrement='auto', index = True)
    eid = Column(Integer, ForeignKey('employee.id'), nullable = False)
    first_line = Column(String, nullable= False)
    second_line = Column(String)
    land_mark = Column(String)
    phone = Column(String, nullable = False)
    city = Column(String, nullable = False)
    pincode = Column(String, nullable = False)
    state = Column(String, nullable = False)
    is_primary = Column(Boolean, default = True)
    created_at = Column(DateTime(), default = datetime.now())
    updated_at = Column(DateTime(), onupdate = datetime.now(), default = datetime.now())

    def __init__(self, id = None, eid = None, first_line = None, second_line = None, phone = None, land_mark = None, city = None, pincode = None, state = None):
        self.id = id
        self.eid = eid
        self.first_line = first_line
        self.second_line = second_line
        self.phone = phone
        self.land_mark = land_mark
        self.city = city
        self.pincode = pincode
        self.state = state


class Employee(Base):
    __tablename__ = 'employee'

    id = Column(Integer, primary_key = True, autoincrement='auto', index = True)
    eid = Column(String, unique= True, nullable = False)
    firstname = Column(String, nullable = False)
    lastname = Column(String, nullable = False)
    contact = Column(String, nullable=False, unique=True)
    is_approved = Column(Boolean, default = False)
    office_mail = Column(String)
    designation = Column(String, nullable = False)
    approved_by = Column(Integer)
    approved_at = Column(DateTime())
    deleted_by = Column(Integer)
    deleted_at = Column(DateTime())
    created_by = Column(Integer, nullable = False)
    is_deleted = Column(Boolean, default = False)
    created_at = Column(DateTime(), default = datetime.now())
    updated_at = Column(DateTime(), onupdate = datetime.now(), default = datetime.now())
    dept_id = Column(Integer, ForeignKey("department.id"), nullable = False)

    def __init__(self, id = None, eid = None, office_mail = None, firstname = None, lastname = None, contact = None, created_by = None, dept_id = None, designation = None):
        self.id = id
        self.eid = eid
        self.office_mail = office_mail
        self.lastname = lastname
        self.contact = contact
        self.firstname = firstname
        self.created_by = created_by
        self.dept_id = dept_id
        self.designation = designation
