from django.shortcuts import render

# Create your views here.
def admin_home(request):
    return render(request, 'admin_home.html')

def client_management(request):
    return render(request, "clients_management.html")