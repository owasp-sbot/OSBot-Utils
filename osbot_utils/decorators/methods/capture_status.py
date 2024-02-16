from functools import wraps

def capture_status(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        try:
            # Attempt to execute the method
            result = method(*args, **kwargs)
            return {'status': 'ok', 'data': result}
        except Exception as error:
            # Handle any exceptions that occur
            return {'status': 'error', 'error': str(error)}
    return wrapper


def apply_capture_status(cls):
    for attr_name, attr_value in cls.__dict__.items():
        if callable(attr_value) and not attr_name.startswith("__"):
            setattr(cls, attr_name, capture_status(attr_value))
    return cls