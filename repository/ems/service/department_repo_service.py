from sqlalchemy.orm import Session
from api.exception.errors import DataNotFoundException
from repository.ems.model.ems import Department
from datetime import datetime

from service.utils.message_utils import MessageUtils


class DepartmentRepoService:
    def save(dept : Department, db : Session):
        db.add(dept)
        db.commit()
    
    def update(dept : Department, db : Session):
        db.query(Department).filter(Department.id == dept.id).update({Department.name : dept.name,
                                      Department.description : dept.description, 
                                      Department.is_approved : dept.is_approved,
                                      Department.is_deleted : dept.is_deleted
                                      })
        db.commit()

    def fetchByName(name : str, db : Session):
        return db.query(Department).filter(Department.name == name).first()
    
    def fetchById(id : int, db : Session):
        return db.query(Department).filter(Department.id == id).first()
    
    def validateAndGetByName(name : str, db : Session):
        dept =  db.query(Department).filter(Department.name == name).first()
        if dept is None:
            raise DataNotFoundException(MessageUtils.entity_not_found('Department','name', name))
        return dept
    
    def validateAndGetById(id : int, db : Session):
        dept = db.query(Department).filter(Department.id == id).first()
        if dept is None:
            raise DataNotFoundException(MessageUtils.entity_not_found('Department','id', id))
        return dept
    
    def softDeleteById(id : int, uid : int, db : Session):
        db.query(Department).filter(Department.id == id).update({Department.is_deleted : True, Department.deleted_by : uid, Department.deleted_at : datetime.now()})
        db.commit()
    
    def restoreById(id : int, db : Session):
        db.query(Department).filter(Department.id == id).update({Department.is_deleted : False, Department.deleted_at : None, Department.deleted_by : None})
        db.commit()
    
    def approveById(id : int, uid : int, db : Session):
        db.query(Department).filter(Department.id == id).update({Department.is_approved : True, Department.approved_at : datetime.now(), Department.approved_by : uid})
        db.commit()
    
    def deleteById(id: int, db : Session):
        db.query(Department).filter(Department.id == id).delete()
        db.commit()
    
    def fetchAll(db : Session):
        return db.query(Department).filter(Department.is_deleted == False).all()
    
    def validateAndGetAll(db : Session):
        depts = db.query(Department).filter(Department.is_deleted == False).all()
        if len(depts) == 0:
            raise DataNotFoundException(MessageUtils.entities_not_found('Departments'))
        return depts
    