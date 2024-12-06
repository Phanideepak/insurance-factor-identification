class ServiceException(Exception):
     def __init__(self, status_message = None, status_code = None, errorMessage = None):
          self.status_code = status_code if status_code else 500
          self.status_message = status_message if status_message else 'Internal Error Occured'
          self.error_message = errorMessage if errorMessage else 'Internal Error Occured'

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