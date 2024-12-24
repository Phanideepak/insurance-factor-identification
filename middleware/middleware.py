import secrets
from fastapi import Request
from fastapi.responses import StreamingResponse
from config import nosql_db
from datetime import datetime
from starlette.middleware.base import BaseHTTPMiddleware
import json




class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request : Request, call_next):
        db = nosql_db.get_database()
        request_log_collection = db['request_logs']
        request_body = None

        try:
            body_bytes = await request.body()
            if body_bytes:
                request_body = json.loads(body_bytes.decode('utf-8'))
        except json.JSONDecodeError:
            request_body = None


        query_params = dict(request.query_params)
        path_params = request.path_params
        path = request.url.path
        method = request.method
        headers = dict(request.headers)
        request_id = secrets.token_hex(16)
        

        log_entry = {
            'api' : path,
            'method' : method,
            'headers' : headers,
            'query_params' : query_params,
            'path_params' : path_params,
            'request_id' : request_id,
            'body' : request_body,
            'request_timestamp': datetime.now()
        }

        response = await call_next(request)

        await request_log_collection.insert_one(log_entry)

        response_body = b""

        async for chunk in response.body_iterator:
            response_body += chunk
        
        response_body_text = response_body.decode('utf-8')

        response_content_type = response.headers.get('Content-Type','')

        log_entry = await request_log_collection.find_one({'request_id' : request_id})

        response_dict = {}

        response_dict['status_code'] = response.status_code


        if 'application/json' in response_content_type:
            try:
               json_body = json.loads(response_body_text) if response_body_text else None
            except:
                json_body = None
        elif 'text/html' in response_content_type:
            response_dict['html'] = response_body_text
        else:
            response_dict['raw'] = response_body_text


        if 'exception' in json_body:
            response_dict['error_message'] = json_body['exception']
        
        if 'status_message' in json_body:
            response_dict['status_message'] = json_body['status_message']
        
        if 'exception_id' in json_body:
            response_dict['exception_id'] = json_body['exception_id']
        
        if 'data' in json_body:
            response_dict['response_body'] = json_body['data']
     

        await request_log_collection.update_one({'request_id' : request_id}, {'$set' : response_dict})
        

        return StreamingResponse(iter([response_body]), status_code=response.status_code, headers=dict(response.headers))
    