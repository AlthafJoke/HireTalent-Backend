from django.http import JsonResponse

def handler500(request):
    print("working handler")
    message = ('internal server error')
    response = JsonResponse(data={ 'error': message })
    
    response.status_code = 500
    
    return response