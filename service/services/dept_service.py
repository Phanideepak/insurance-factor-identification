from api.exception.errors import NotModifiedException, ServiceException, ValidationException
from repository.ems.service.department_repo_service import DepartmentRepoService
from repository.ems.service.user_repo_service import UserRepoService
from repository.ems.model.ems import Department
from api.dto.dto import AddDepartmentBody,UpdateDepartmentBody
from sqlalchemy.orm import Session
from service.utils.message_utils import MessageUtils
from service.utils.response_util import ResponseUtils
from service.mapper.mapper import departmentModelToDepartmentDto, departmentModelToDepartmentDtoList
from redis import Redis
from service.utils.validation_utils import ValidationUtils
        

class DeptService:

    def add(request : AddDepartmentBody, logged_user, db : Session):
        user = UserRepoService.validateAndGetByEmail(logged_user, db)
        if DepartmentRepoService.fetchByName(request.name, db) is not None:
            raise ValidationException(MessageUtils.entity_already_exists('Department','name', request.name))
        try:
            DepartmentRepoService.save(Department(name= request.name, description = request.description, created_by = user.id), db)
        except Exception as e:
            raise ServiceException(str(e))
        
        return ResponseUtils.wrap('added successfully')
    

    def update(request : UpdateDepartmentBody, db : Session):
        curr_dept = DepartmentRepoService.validateAndGetById(request.id, db)
        
        is_updated = False

        if curr_dept.name != request.name:
            curr_dept.name = request.name
            is_updated = True
        
        if curr_dept.description != request.description:
            curr_dept.description = request.description
            is_updated = True
        
        if not is_updated:
           raise NotModifiedException()

        try:
            DepartmentRepoService.update(curr_dept, db)
        except Exception as e:
            raise ServiceException(str(e))
        
        return ResponseUtils.wrap('updated successfully')


    def getById(id : int, db : Session):
        return ResponseUtils.wrap(departmentModelToDepartmentDto(DepartmentRepoService.validateAndGetById(id, db)))
    
    def fetchById(id : int, db : Session):
        return departmentModelToDepartmentDto(DepartmentRepoService.fetchById(id, db))

    def deleteById(id : int, logged_user, db : Session):
        user = UserRepoService.validateAndGetByEmail(logged_user, db)
        dept = DepartmentRepoService.validateAndGetById(id, db)
        

        ValidationUtils.isTrue(not dept.is_deleted, 'Already Deleted!')

        try:
            DepartmentRepoService.softDeleteById(id, user.id, db)
        except Exception as e:
           raise ServiceException(str(e))

        return ResponseUtils.wrap('Deleted successfully')
    
    def restoreById(id : int, db : Session):
        dept = DepartmentRepoService.validateAndGetById(id, db)
        
        ValidationUtils.isTrue(dept.is_deleted, 'Already Restored!')

        try:
            DepartmentRepoService.restoreById(id, db)
        except Exception as e:
            raise ServiceException(str(e))

        return ResponseUtils.wrap('Restored successfully')
    
    def approveById(id : int, logged_user, db : Session):
        user = UserRepoService.validateAndGetByEmail(logged_user, db)
        dept = DepartmentRepoService.validateAndGetById(id, db)
        
        ValidationUtils.isTrue(not dept.is_approved, 'Already Approved!')

        try:
            DepartmentRepoService.approveById(id, user.id, db)
        except Exception as e:
            raise ServiceException(str(e))

        return ResponseUtils.wrap('Restored successfully')


    def getAll(db : Session, cache : Redis):
        depts = []
        # if CacheService.has(CacheKey.ALL_DEPARTMENTS.name, cache):
        #     depts = CacheService.get(CacheKey.ALL_DEPARTMENTS.name, cache)
        #     if depts is not None and len(depts) > 0:
        #         return ResponseUtils.wrap(departmentCacheToDepartmentDtoList(depts))
                
        depts = DepartmentRepoService.validateAndGetAll(db)
        # CacheService.put(CacheKey.ALL_DEPARTMENTS.name, depts, cache)
       

        return ResponseUtils.wrap(departmentModelToDepartmentDtoList(depts))
    
    def fetchAll(db : Session, cache : Redis):
        depts = []

        # if CacheService.has(CacheKey.ALL_DEPARTMENTS.name, cache):
        #     depts = CacheService.get(CacheKey.ALL_DEPARTMENTS.name, cache)
        #     return departmentCacheToDepartmentDtoList(depts)
        
        depts = DepartmentRepoService.validateAndGetAll(db)
        #CacheService.put(key = CacheKey.ALL_DEPARTMENTS.name, value = depts, cache = cache, jsonSerializer = Department.json_serializer)     

        return departmentModelToDepartmentDtoList(depts)
