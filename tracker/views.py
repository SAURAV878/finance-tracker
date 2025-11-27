from django.shortcuts import render

# Create your views here.
# views = handle requets and response of function

def dashboard(request): #request = object conating info about HTTP request
    return render(request, 'tracker/dashboard.html')