
from api.dto.dto import AddAgentRequest, UpdateAgentRequest
from sqlalchemy.orm import Session

from api.exception.errors import NotModifiedException, ServiceException
from repository.insurance.model.insurance import User
from repository.insurance.service.agent_repo_service import AgentRepoService
from repository.insurance.service.user_repo_service import UserRepoService
from service.mapper.mapper import Mapper, ResponseMapper
from service.utils.response_util import ResponseUtils
from passlib.context import CryptContext
from service.utils.update_utils import UpdateUtils

bcryptContext = CryptContext(schemes=['bcrypt'])

class AgentService:
    def add_agent(request : AddAgentRequest, db : Session):
        try:
            AgentRepoService.insert(Mapper.toAgent(request), db)
            UserRepoService.insert(User(request.email, request.firstname, request.lastname, bcryptContext.hash('agent123'), 'ROLE_AGENT'),db)
        except Exception as e:
            raise ServiceException(errorMessage = str(e))
        return ResponseUtils.wrap('Agent added successfully')
        

    def update_agent(request : UpdateAgentRequest, db : Session):
        is_updated = False

        agent = AgentRepoService.validate_and_get_by_id(request.id, db)

        if UpdateUtils.is_different(request.firstname, agent.firstname):
            is_updated = True
            agent.firstname = request.firstname

        if UpdateUtils.is_different(request.lastname, agent.lastname):
            is_updated = True
            agent.lastname = request.lastname

        if UpdateUtils.is_different(request.email, agent.email):
            is_updated = True
            agent.email = request.email 

        if UpdateUtils.is_different(request.phone, agent.phone):
            is_updated = True
            agent.phone = request.phone        
        
        if not is_updated:
            raise NotModifiedException()

        AgentRepoService.update(agent, db)

        return ResponseUtils.wrap('Agent updated successfully')


    @classmethod
    def get_by_id(cls, id, db : Session):
        agent = AgentRepoService.validate_and_get_by_id(id, db)
        return ResponseUtils.wrap(ResponseMapper.toAgentDto(agent)) 

    @classmethod
    def get_all(cls, db : Session):
        agents = AgentRepoService.validate_and_get_all(db)
        return ResponseUtils.wrap(ResponseMapper.toAgentDtos(agents))

    def delete_by_id(id, db : Session):
        agent = AgentRepoService.validate_and_get_by_id(id, db)
        AgentRepoService.delete_by_id(agent.id, db)
        return ResponseUtils.wrap('Deleted Successfully')