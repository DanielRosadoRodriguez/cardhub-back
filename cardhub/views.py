import json

from cardhub.domain.Authenticator import Authenticator
from .models import User
from .models import CardHolder
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def sign_up(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            newUser = _createUser(data)
            _saveUser(newUser)
        except json.JSONDecodeError as e:
            print("Error analyzing JSON: ", e)
        return HttpResponse("Form submitted successfully!")
    else:
        return HttpResponse("Invalid form submission method")
    

@csrf_exempt
def log_in(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data['email']
            password = data['password']
            authenticator = Authenticator(email, password)
            is_authenticated = authenticator.authenticate_user()
            print(is_authenticated)
        except json.JSONDecodeError as e:
            print("Error analyzing JSON: ", e)  
        return HttpResponse("Form submitted successfully!")
    else:
        return HttpResponse("Invalid form submission method")

        
def _createUser(data):
    name = data['name']
    email = data['email']
    password = data['password']
    newUser = User(name=name, email=email, password=password)
    return newUser

def _saveUser(newUser):
    newUser.save()

def _createCardHolderForUser(user: User) -> CardHolder:
    card_holder = CardHolder(user=user)
    card_holder.save()
    return card_holder

def test_create_cardholder(request):
    user = _createUser({'name': 'joselito', 'email': 'joselito@gmail.com', 'password': '123456'})
    _saveUser(user)
    _createCardHolderForUser(user)
    return HttpResponse("Cardholder created successfully!")