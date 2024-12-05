from api.exception.errors import NotModifiedException, ServiceException, ValidationException
from repository.ems.service.employment_repo_service import EmployeeRepoService
from repository.ems.service.department_repo_service import DepartmentRepoService
from repository.ems.service.user_repo_service import UserRepoService
from repository.ems.model.ems import Employee, User
from api.dto.dto import AddEmployeeRequest, UpdateEmployeeRequest
from sqlalchemy.orm import Session
from service.utils.message_utils import MessageUtils
from service.utils.response_util import ResponseUtils
from service.mapper.mapper import employeeModelToEmployeeDto
from http import HTTPStatus
from passlib.context import CryptContext
from datetime import datetime

from service.utils.validation_utils import ValidationUtils

bcryptContext = CryptContext(schemes=['bcrypt'])

class EmployeeService:
    def add(request : AddEmployeeRequest, logged_user, role, db : Session):
        user = UserRepoService.validateAndGetByEmail(logged_user, db)
        dept = DepartmentRepoService.validateAndGetById(request.dept_id, db)

        if role == 'ROLE_ADMIN' and dept.name != 'HR':
            raise ValidationException('Admin Users can only recruit HR Employees')
        
        if role == 'ROLE_HR' and dept.name == 'HR':
            raise ValidationException('HR Users cannot recruit HR Employees')


        try:
            EmployeeRepoService.save(Employee(firstname = request.firstname, lastname = request.lastname, designation = request.designation, contact = request.contact, created_by = user.id, dept_id = dept.id, eid = request.eid), db)
        except Exception as e:
            raise ServiceException(str(e))
        
        return ResponseUtils.wrap('added successfully')
    

    def update(request : UpdateEmployeeRequest, logged_user, role, db : Session):
        user = UserRepoService.validateAndGetByEmail(logged_user, db)
        emp = EmployeeRepoService.validateAndGetByEid(request.eid, db)

        curr_dept = DepartmentRepoService.validateAndGetById(emp.dept_id, db)
        

        if role == 'ROLE_ADMIN' and curr_dept.name != 'HR':
            raise ValidationException('Admin Users can only edit HR Employees')
        
        if role == 'ROLE_HR' and curr_dept.name == 'HR':
            raise ValidationException('HR Users cannot edit HR Employees')
        
        is_updated = False

        if request.firstname != emp.firstname:
            emp.firstname = request.firstname
            is_updated = True
        
        if request.lastname != emp.lastname:
            emp.lastname = request.lastname
            is_updated = True

        if request.contact != emp.contact:
            emp.contact = request.contact
            is_updated = True
        
        if request.dept_id != emp.dept_id:
            emp.dept_id = request.dept_id
            is_updated = True

        if request.designation != emp.designation:
            emp.designation = request.designation
            is_updated = True
        
        if not is_updated:
           raise NotModifiedException()

        try:
            EmployeeRepoService.update(emp, db)
        except Exception as e:
            raise ServiceException(str(e))
        
        return ResponseUtils.wrap('updated successfully')


    def getById(id : int, db : Session):
        emp = EmployeeRepoService.validateAndGetById(id, db)
        dept = DepartmentRepoService.validateAndGetById(emp.dept_id, db)
        return ResponseUtils.wrap(employeeModelToEmployeeDto(emp, dept, UserRepoService.validateAndGetById(emp.created_by, db), UserRepoService.fetchById(emp.deleted_by, db), UserRepoService.fetchById(emp.approved_by, db) ))

    def fetchById(id : int, db : Session): 
        emp = EmployeeRepoService.validateAndGetById(id, db) 
        return employeeModelToEmployeeDto(emp, DepartmentRepoService.validateAndGetById(emp.dept_id, db),UserRepoService.validateAndGetById(emp.created_by, db), UserRepoService.fetchById(emp.deleted_by, db), UserRepoService.fetchById(emp.approved_by, db) )

    def deleteById(id : int, logged_user, db : Session):
        user = UserRepoService.validateAndGetByEmail(logged_user, db)
        emp = EmployeeRepoService.validateAndGetById(id, db)
        
        ValidationUtils.isTrue(not emp.is_deleted, 'Already Deleted!')

        try:
            EmployeeRepoService.softDeleteById(id, user.id, db)
        except Exception as e:
            raise ServiceException(str(e))

        return ResponseUtils.wrap('Deleted successfully')
    
    def restoreById(id : int, db : Session):
        emp = EmployeeRepoService.validateAndGetById(id, db)
        
        ValidationUtils.isTrue(emp.is_deleted, 'Already Restored!')

        try:
            EmployeeRepoService.restoreById(id, db)
        except Exception as e:
            raise ServiceException(str(e))

        return ResponseUtils.wrap('Restored successfully')
    
    def approveById(id : int, logged_user, role, db : Session):   
        user = UserRepoService.validateAndGetByEmail(logged_user, db)    
        emp = EmployeeRepoService.validateAndGetById(id, db)
        
        dept = DepartmentRepoService.getById(emp.dept_id, db)

        if role == 'ROLE_ADMIN' and dept.name != 'HR':
            raise ValidationException('Admin Users can only approve HR Employees')
        
        if role == 'ROLE_HR' and dept.name == 'HR':
            raise ValidationException('HR Users cannot approve HR Employees')
    

        ValidationUtils.isTrue(not emp.is_approved, 'Already Approved!')

        emp_role = 'ROLE_EMPLOYEE'

        if role == 'ROLE_ADMIN':
            emp_role = 'ROLE_HR'

        try:
            emp.office_mail = f'{emp.firstname}.{emp.lastname}.{emp.eid}@lincom.com'
            emp.is_approved = True
            emp.approved_at = datetime.now()
            emp.approved_by = user.id

            EmployeeRepoService.update(emp, db)
            
            UserRepoService.save(User(firstname = emp.firstname, lastname = emp.lastname, email = emp.office_mail, password = bcryptContext.hash('abc@123'), role = emp_role), db)
        except Exception as e:
            raise ServiceException(str(e))

        return ResponseUtils.wrap('approved successfully')


    def getAll(db : Session):
        emps = EmployeeRepoService.validateAndGetAll(db)
        empDtos = []

        for emp in emps:
            empDtos.append(employeeModelToEmployeeDto(emp, DepartmentRepoService.validateAndGetById(emp.dept_id, db), UserRepoService.validateAndGetById(emp.created_by, db), UserRepoService.fetchById(emp.deleted_by, db), UserRepoService.fetchById(emp.approved_by, db) ))

        return ResponseUtils.wrap(empDtos)

    def fetchAll(db : Session):
        emps = EmployeeRepoService.fetchAll(db)
        empDtos = []

        for emp in emps:
            empDtos.append(employeeModelToEmployeeDto(emp, DepartmentRepoService.validateAndGetById(emp.dept_id, db), UserRepoService.validateAndGetById(emp.created_by, db), UserRepoService.fetchById(emp.deleted_by, db), UserRepoService.fetchById(emp.approved_by, db) ))

        return empDtos