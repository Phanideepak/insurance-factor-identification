from sqlalchemy.orm import Session
from api.exception.errors import DataNotFoundException
from repository.ems.model.ems import Employee
from datetime import datetime

from service.utils.message_utils import MessageUtils


class EmployeeRepoService:
    def save(employee : Employee, db : Session):
        db.add(employee)
        db.commit()
    
    def update(employee : Employee, db : Session):
        db.query(Employee).filter(Employee.id == employee.id).update({
                                      Employee.firstname : employee.firstname,
                                      Employee.lastname : employee.lastname,  
                                      Employee.office_mail : employee.office_mail, 
                                      Employee.contact : employee.contact,
                                      Employee.dept_id : employee.dept_id,
                                      Employee.created_by : employee.created_by,
                                      Employee.approved_at : employee.approved_at,
                                      Employee.approved_by : employee.approved_by,
                                      Employee.is_approved : employee.is_approved  
                                      })
        db.commit()

    def fetchByEid(eid : str, db : Session):
        return db.query(Employee).filter(Employee.eid == eid).first()
    
    def fetchByOfficeMail(office_mail : str, db : Session):
        return db.query(Employee).filter(Employee.office_mail == office_mail).first()
    
    def fetchById(id : int, db : Session):
        return db.query(Employee).filter(Employee.id == id).first()
    
    def validateAndGetByEid(eid : str, db : Session):
        emp = db.query(Employee).filter(Employee.eid == eid).first()
        if emp is None:
            raise DataNotFoundException(MessageUtils.entity_not_found('employee','eid',eid))
        return emp
    
    def validateAndGetByOfficeMail(office_mail : str, db : Session):
        emp =  db.query(Employee).filter(Employee.office_mail == office_mail).first()
        if emp is None:
            raise DataNotFoundException(MessageUtils.entity_not_found('employee','office_mail',office_mail))
        return emp
    
    def validateAndGetById(id : int, db : Session):
        emp =  db.query(Employee).filter(Employee.id == id).first()
        if emp is None:
            raise DataNotFoundException(MessageUtils.entity_not_found('employee','id',id))
        return emp
    
    def softDeleteById(id : int, uid : int, db : Session):
        db.query(Employee).filter(Employee.id == id).update({Employee.is_deleted : True, Employee.deleted_by : uid, Employee.deleted_at : datetime.now()})
        db.commit()
    
    def restoreById(id : int, db : Session):
        db.query(Employee).filter(Employee.id == id).update({Employee.is_deleted : False, Employee.deleted_at : None, Employee.deleted_by : None})
        db.commit()
    
    def approveById(id : int, uid : int, db : Session):
        db.query(Employee).filter(Employee.id == id).update({Employee.is_approved : True, Employee.approved_at : datetime.now(), Employee.approved_by : uid})
        db.commit()

    def fetchAll(db : Session):
        return db.query(Employee).filter(Employee.is_deleted == False).all()

    def validateAndGetAll(db : Session):
        emps = db.query(Employee).filter(Employee.is_deleted == False).all()
        if len(emps) == 0:
            raise DataNotFoundException(MessageUtils.entities_not_found('employees'))
        return emps