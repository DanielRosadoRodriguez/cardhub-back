import json
from .models import UserWithWallet
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def submit_form(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            newUserWithWallet = createUser(data)
            newUserWithWallet.save()
        except json.JSONDecodeError as e:
            print("Error al analizar JSON:", e)
        return HttpResponse("Form submitted successfully!")
    else:
        return HttpResponse("Invalid form submission method")
    

def createUser(data):
    name = data['name']
    email = data['email']
    password = data['password']
    newUserWithWallet = UserWithWallet(name, email, password)
    return newUserWithWallet