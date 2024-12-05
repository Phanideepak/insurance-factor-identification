class MessageUtils:
    def invalid_password():
        return 'Invalid password'
    
    def login_success_message():
        return 'Login Successfully.'
    
    def signup_success_message():
        return 'user created successfully'

    def entity_already_exists(entity_name, field_name, val):
        return f'{entity_name} with {field_name} : {val} already exists'
    
    def entities_not_found(entity_name):
        return f'No {entity_name} found'
    
    def fields_not_modified():
        return 'Fields Not Modified'
    
    def entity_not_found(entity_name, field_name, val):
        return f'No {entity_name} Found by {field_name} : {val}'
    
    def entity_not_found_two(entity_name, field_name, val, second_field_name, second_val):
        return f'No {entity_name} Found by {field_name} : {val}  and {second_field_name} : {second_val}'