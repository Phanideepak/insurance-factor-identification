
from api.dto.dto import AddAgentRequest, UpdateAgentRequest
from sqlalchemy.orm import Session

from service.services.agent_service import AgentService
from service.utils.validation_utils import ValidationUtils


class AgentExecutor:
    
    def add_agent(request : AddAgentRequest, db : Session):
        ValidationUtils.isEmpty(request.firstname, 'firstname')
        request.firstname = request.firstname.strip()
        ValidationUtils.isEmpty(request.lastname, 'lastname')
        ValidationUtils.isEmpty(request.email, 'email')
        request.email = request.email.strip()
        ValidationUtils.isEmpty(request.phone, 'phone')
        request.phone = request.phone.strip()

        return AgentService.add_agent(request, db)

    def update_agent(request : UpdateAgentRequest, db : Session):
        ValidationUtils.isZero(request.id, 'agent_id')
        ValidationUtils.isEmpty(request.firstname, 'firstname')
        request.firstname = request.firstname.strip()
        ValidationUtils.isEmpty(request.lastname, 'lastname')
        request.lastname = request.lastname.strip()
        ValidationUtils.isEmpty(request.email, 'email')
        request.email = request.email.strip()
        ValidationUtils.isEmpty(request.phone, 'phone')
        request.phone = request.phone.strip()
        
        return AgentService.update_agent(request, db)

    def get_by_id(id, db : Session):
        ValidationUtils.isZero(id, 'id')
        
        return AgentService.get_by_id(id, db)

    def get_all(db : Session):
        return AgentService.get_all(db)

    def delete_by_id(id, db : Session):
        ValidationUtils.isZero(id, 'id')

        return AgentService.delete_by_id(id, db)