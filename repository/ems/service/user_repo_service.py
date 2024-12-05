from repository.ems.model.ems import User
from api.exception.errors import DataNotFoundException
from sqlalchemy.orm import Session

from service.utils.message_utils import MessageUtils


class UserRepoService:
    def save(user : User, db : Session):
        db.add(user)
        db.commit()
    
    def update(user : User, db : Session):
        db.query(User).filter(User.id == user.id).update({User.firstname : user.firstname,
                                      User.lastname : user.lastname, 
                                      User.email : user.email, User.password : user.password})
        db.commit()
    
    def fetchByEmail(email : str, db : Session):
        return db.query(User).filter(User.email == email).first()

    def validateAndGetByEmail(email : str, db : Session):
        user = db.query(User).filter(User.email == email).first()

        if user is None:
            raise DataNotFoundException(MessageUtils.entity_not_found('User','email', email))

        return user
    
    def fetchById(id : int, db : Session):
        return db.query(User).filter(User.id == id).first()
    
    def validateAndGetById(id : int, db : Session):
        user =  db.query(User).filter(User.id == id).first()
        
        if user is None:
            raise DataNotFoundException(MessageUtils.entity_not_found('Users','id',id))
        return user
    
    def deleteById(id: int, db : Session):
        db.query(User).filter(User.id == id).delete()
        db.commit()
    
    def fetchAll(db : Session):
        return db.query(User).all()
    
    def validateAndGetAll(db : Session):
        users = db.query(User).all()
        if len(users) == 0:
            raise DataNotFoundException(MessageUtils.entities_not_found('Users'))
        return users