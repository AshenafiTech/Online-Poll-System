from django.http import HttpResponse

def home(request):
    return HttpResponse('<h1>Welcome to the Online Poll System!</h1>')
