from fastapi import APIRouter, Depends, Response
from api.dto.dto import AddAgentRequest, UpdateAgentRequest
from config import database
from sqlalchemy.orm import Session
from app_secrets.service.dependencies import AccessTokenBearer, RoleChecker
from service.executor.agent_executor import AgentExecutor



class AgentController:
    router = APIRouter(prefix='/agent', tags=['Agent API'])
    get_db = database.get_db
    access_token_bearer = AccessTokenBearer()

    @router.post('', summary='Add Agent API', dependencies=[Depends(RoleChecker(['ROLE_ADMIN']))])    
    def add_agent(request : AddAgentRequest, resp : Response, db : Session = Depends(get_db), token_details = Depends(access_token_bearer)):
        responseBody = AgentExecutor.add_agent(request, db)
        resp.status_code = responseBody.status_code

        return responseBody.dict(exclude_none = True)
    
    @router.put('', summary= 'Update Agent API', dependencies=[Depends(RoleChecker(['ROLE_ADMIN']))])
    def update_agent(request : UpdateAgentRequest, resp : Response, db : Session = Depends(get_db), token_details = Depends(access_token_bearer)):
        responseBody = AgentExecutor.update_agent(request, db)
        resp.status_code = responseBody.status_code

        return responseBody.dict(exclude_none = True)

    @router.delete('', summary = 'Delete Agent by Id', dependencies = [Depends(RoleChecker(['ROLE_ADMIN']))])
    def delete_by_id(id : int, resp : Response, db : Session = Depends(get_db), token_details = Depends(access_token_bearer)):
        responseBody = AgentExecutor.delete_by_id(id, db)
        resp.status_code = responseBody.status_code

        return responseBody.dict(exclude_none = True)     
    
    
    @router.get('', summary = 'Get Agent by Id', dependencies = [Depends(RoleChecker(['ROLE_ADMIN', 'ROLE_AGENT']))])
    def get_agent_by_id(id : int, resp : Response, db : Session = Depends(get_db), token_details = Depends(access_token_bearer)):
        responseBody = AgentExecutor.get_by_id(id, db)
        resp.status_code = responseBody.status_code

        return responseBody.dict(exclude_none = True) 

    @router.get('/all', summary = 'Get All Agents', dependencies = [Depends(RoleChecker(['ROLE_ADMIN']))])
    def get_all_agents(resp : Response, db : Session = Depends(get_db), token_details = Depends(access_token_bearer)):
        responseBody = AgentExecutor.get_all(db)
        resp.status_code = responseBody.status_code

        return responseBody.dict(exclude_none = True)