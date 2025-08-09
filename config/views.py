from django.http import JsonResponse

def home(request):
    return JsonResponse({
        'message': 'Online Poll System API',
        'endpoints': {
            'api': '/api/',
            'swagger': '/swagger/',
            'redoc': '/redoc/',
            'admin': '/admin/'
        }
    })
