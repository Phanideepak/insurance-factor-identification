def singleton(cls):
    object_map = {}
    def get_instance(*args, **kwargs):
        if cls not in object_map:
            object_map[cls] = cls(*args, **kwargs)
        
        return object_map[cls]
    
    return get_instance