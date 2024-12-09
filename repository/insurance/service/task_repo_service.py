from sqlalchemy.orm import Session

from api.exception.errors import DataNotFoundException
from repository.insurance.model.insurance import Task
from service.utils.message_utils import MessageUtils


class TaskRepoService:
    
    def insert(task, db : Session):
        db.add(task)
        db.commit()
    
    def update(task : Task, db : Session):
        db.query(Task).filter(Task.id == task.id).update({Task.order_id : task.order_id, Task.premium_amount_to_pay : task.premium_amount_to_pay, Task.premium_amount_paid : task.premium_amount_paid, Task.premium_type : task.premium_type, Task.premium_penalty : task.premium_penalty, Task.task_status : task.task_status, Task.payment_status : task.payment_status, Task.paid_at : task.paid_at})
        db.commit()
    
    def fetch_by_id(id, db : Session):
        return db.query(Task).filter(Task.id == id).first()

    def fetch_by_order_id(order_id, db : Session):
        return db.query(Task).filter(Task.order_id == order_id).all()
    
    def validate_and_get_by_order_id(order_id, db : Session):
        tasks =  db.query(Task).filter(Task.order_id == order_id).all()
        if not tasks:
           raise DataNotFoundException(MessageUtils.entity_not_found('Tasks', 'order_id', order_id))
        return tasks 

    def fetch_all(db : Session):
        return db.query(Task).all()

    @classmethod
    def validate_and_get_by_id(cls, id, db : Session):
        task = cls.fetch_by_id(id, db)
        if task is None:
            raise DataNotFoundException(MessageUtils.entity_not_found('Task', 'id', id))

        return task


    @classmethod
    def validate_and_get_all(cls, db : Session):
        tasks = cls.fetch_all(db)
        if not tasks:
            raise DataNotFoundException(MessageUtils.entities_not_found('Tasks'))

        return tasks


    def delete_by_id(id, db : Session):
        db.query(Task).filter(Task.id == id).delete()
        db.commit()