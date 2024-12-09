from sqlalchemy.orm import Session

from api.exception.errors import DataNotFoundException
from repository.insurance.model.insurance import Agent
from service.utils.message_utils import MessageUtils


class AgentRepoService:
    
    def insert(agent, db : Session):
        db.add(agent)
        db.commit()
    
    def update(agent, db : Session):
        db.query(Agent).filter(Agent.id == agent.id).update({Agent.firstname : agent.firstname, Agent.lastname : agent.lastname,  Agent.email : agent.email, Agent.phone  : agent.phone})
        db.commit()
    
    def fetch_by_id(id, db : Session):
        return db.query(Agent).filter(Agent.id == id).first()
    
    def fetch_by_email(email, db : Session):
        return db.query(Agent).filter(Agent.email == email).first()
    
    def fetch_all(db : Session):
        return db.query(Agent).all()

    @classmethod
    def validate_and_get_by_id(cls, id, db : Session):
        agent = cls.fetch_by_id(id, db)
        if agent is None:
            raise DataNotFoundException(MessageUtils.entity_not_found('Agent', 'id', id))

        return agent
    
    @classmethod
    def validate_and_get_by_email(cls, email, db : Session):
        agent = cls.fetch_by_email(email, db)
        if agent is None:
            raise DataNotFoundException(MessageUtils.entity_not_found('Agent', 'email', email))

        return agent

    @classmethod
    def validate_and_get_all(cls, db : Session):
        agents = cls.fetch_all(db)
        if not agents:
            raise DataNotFoundException(MessageUtils.entities_not_found('Agents'))

        return agents


    def delete_by_id(id, db : Session):
        db.query(Agent).filter(Agent.id == id).delete()
        db.commit()