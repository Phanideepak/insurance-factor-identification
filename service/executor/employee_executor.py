from service.utils.validation_utils import ValidationUtils
from service.services.employee_service import EmployeeService
from api.dto.dto import AddEmployeeRequest
from sqlalchemy.orm import Session



class EmployeeExecutor:
      def add(request : AddEmployeeRequest, logged_user, role, db : Session):
            ValidationUtils.isEmpty(request.firstname, 'firstname')
            request.firstname = request.firstname.strip()
            ValidationUtils.isEmpty(request.lastname, 'lastname')
            request.lastname = request.lastname.strip()
            ValidationUtils.isEmpty(request.contact, 'contact')
            request.contact = request.contact.strip()
            ValidationUtils.isEmpty(request.eid, 'eid')
            request.eid = request.eid.strip()
            ValidationUtils.isEmpty(request.designation, 'designation')
            request.designation = request.designation.strip()
            ValidationUtils.isZero(request.dept_id, 'dept_id')

            return EmployeeService.add(request, logged_user, role, db)
      
      def update(request, logged_user, role, db : Session):      
            ValidationUtils.isEmpty(request.firstname, 'firstname')
            request.firstname = request.firstname.strip()
            ValidationUtils.isEmpty(request.lastname, 'lastname')
            request.lastname = request.lastname.strip()
            ValidationUtils.isEmpty(request.contact, 'contact')
            request.contact = request.contact.strip()
            ValidationUtils.isEmpty(request.eid, 'eid')
            request.eid = request.eid.strip()
            ValidationUtils.isEmpty(request.designation, 'designation')
            request.designation = request.designation.strip()
            ValidationUtils.isZero(request.dept_id, 'dept_id')

            return EmployeeService.update(request, logged_user, role, db)

      def getById(id, db : Session):
            ValidationUtils.isZero(id, 'employee_id')
            return EmployeeService.getById(id, db)
      
      def fetchById(id, db : Session):
            return EmployeeService.fetchById(id, db)
      
      def deleteById(id, logged_user, db : Session):
            ValidationUtils.isZero(id, 'employee_id')
            return EmployeeService.deleteById(id, logged_user, db)
      
      def restoreById(id, db : Session):
            ValidationUtils.isZero(id, 'employee_id')
            return EmployeeService.restoreById(id, db)

      def approveById(id, logged_user, role, db : Session):
            ValidationUtils.isZero(id, 'employee_id')
            
            return EmployeeService.approveById(id, logged_user, role, db)
      
      
      def getAll(db : Session):
          return EmployeeService.getAll(db)
      
      def fetchAll(db : Session):
          return EmployeeService.fetchAll(db)
            