from django.shortcuts import render

def admin_home(request):
    return render(request, 'admin_home.html')

def client_home(request):
    return render(request, 'client_home.html')

