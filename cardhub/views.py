from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def submit_form(request):
    if request.method == 'POST':
        email = request.POST['email']
        name = request.POST['name']
        password = request.POST['password']
        
        print(f"Email: {email}")
        print(f"Name: {name}")
        print(f"Password: {password}")

        return HttpResponse("Form submitted successfully!")
    else:
        return HttpResponse("Invalid form submission method")