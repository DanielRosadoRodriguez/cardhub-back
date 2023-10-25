from models import UserWithWallet
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def submit_form(request):
    if request.method == 'POST':
        email = request.POST['email']
        name = request.POST['name']
        password = request.POST['password']
        
        usr: UserWithWallet = UserWithWallet(name=name, email=email, password=password)
        usr.save()

        return HttpResponse("Form submitted successfully!")
    else:
        return HttpResponse("Invalid form submission method")
