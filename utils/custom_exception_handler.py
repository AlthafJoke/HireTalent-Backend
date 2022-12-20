from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    print('custom exception is working')
    response = exception_handler(exc, context)
    
    exception_class = exc.__class__.__name__
    
    print(exception_class)
    
    if exception_class == 'AuthenticationFailed':
        response.data = {
            "error": "invalid email or password please try again"
            
        }
    
    return response
    