class ServiceException(Exception):
     status_code = 500
     status_message = 'Internal Error Occurred'
     error_message = status_message

     def __init__(self, status_message = None, status_code = None, errorMessage = None):
          self.status_code = status_code
          self.status_message = status_message
          self.error_message = errorMessage

class DataNotFoundException(ServiceException):
     def __init__(self, error_message = None):
          self.error_message = error_message
          super().__init__('Data Not Found Error', 404, error_message)

class ValidationException(ServiceException):
     def __init__(self, error_message = None):
          self.error_message = error_message
          super().__init__('Validation Error', 400, error_message)

class NotModifiedException(ServiceException):
     def __init__(self, error_message = 'Fields Not Modified'):
          self.error_message = error_message
          super().__init__('Not Modified Error', 400, error_message)

class TokenException(ServiceException):
     def __init__(self, error_message = None):
          self.error_message = error_message
          super().__init__('Token Error', 400, error_message)

class NoPermissionException(ServiceException):
     def __init__(self, error_message = None):
          self.error_message = error_message
          super().__init__('Permission Error', 403, error_message)