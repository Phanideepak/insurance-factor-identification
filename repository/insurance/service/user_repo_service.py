from api.exception.errors import DataNotFoundException
from repository.insurance.model.insurance import User
from service.utils.message_utils import MessageUtils
from sqlalchemy.orm import Session


class UserRepoService:

    def insert(user, db : Session):
        db.add(user)
        db.commit()
    
    def update(user : User, db : Session):
        db.query(User).filter(User.id == user.id).update({User.firstname : user.firstname, User.lastname : user.lastname, User.email : user.email, User.password : user.password})
        db.commit()

    def fetch_by_email(email, db : Session):
        return db.query(User).filter(User.email == email).first()

    def validate_and_get_by_email(email, db : Session):
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise DataNotFoundException(MessageUtils.entity_not_found('User', 'email', email))

        return user
    
    def fetch_by_id(id, db : Session):
        return db.query(User).filter(User.id == id).first()
    
    def validate_and_get_by_id(id, db : Session):
        user = db.query(User).filter(User.id == id).first()
        if user is None:
           raise DataNotFoundException(MessageUtils.entity_not_found('User', 'id', id))

        return user 