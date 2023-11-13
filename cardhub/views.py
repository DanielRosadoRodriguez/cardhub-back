import json

from cardhub.domain.Authenticator import Authenticator
from django.core.serializers import serialize
from .models import User
from .models import CardHolderCard
from .models import CardHolder
from .models import CreditCardProduct
from .models import AccountStatement
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
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


@csrf_exempt
def add_card_to_user_cardholder(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            card_holder = CardHolder.objects.get(user=data['email'])
            card = CreditCardProduct.objects.get(card_id=data['card_id'])
            _addCardToCardHolder(card_holder, card)
        except json.JSONDecodeError as e:
            print("Error analyzing JSON: ", e)
        return HttpResponse("Form submitted successfully!")
    else:
        return HttpResponse("Invalid form submission method")
    
    
@csrf_exempt
def remove_card_from_user_cardholder(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            card_holder = CardHolder.objects.get(user=data['email'])
            card_to_delete = CreditCardProduct.objects.get(card_id=data['card_id'])
            _removeCardFromCardHolder(card_holder, card_to_delete)
        except json.JSONDecodeError as e:
            print("Error analyzing JSON: ", e)
        return HttpResponse("Form submitted successfully!")
    else:
        return HttpResponse("Invalid form submission method")
        

@csrf_exempt
def generate_card_statement(request):  
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            card_from_cardholder = CardHolderCard.objects.get(card_holder_cards_id=data['card_holder_cards_id'])
            _generate_card_statement(card_from_cardholder)
        except json.JSONDecodeError as e:
            print("Error analyzing JSON: ", e)
        return HttpResponse("Form submitted successfully!")
    else:
        return HttpResponse("Invalid form submission method")


def get_all_cards(request):
    cards = CreditCardProduct.objects.all()
    cards_json = list(cards.values())
    return JsonResponse(cards_json, safe=False)


def _createUser(data):
    name = data['name']
    email = data['email']
    password = data['password']
    newUser = User(name=name, email=email, password=password)
    return newUser


def _saveUser(newUser):
    newUser.save()


def _createCreditCardProduct(data):
    card_name = data['card_name']
    bank_name = data['bank_name']
    interest_rate = data['interest_rate']
    annuity = data['annuity']
    newCreditCardProduct = CreditCardProduct(card_name=card_name, bank_name=bank_name, interest_rate=interest_rate, annuity=annuity)
    return newCreditCardProduct


def _saveCreditCardProduct(newCreditCardProduct):
    newCreditCardProduct.save()
    
    
def _createCardHolderForUser(user: User) -> CardHolder:
    card_holder = CardHolder(user=user)
    card_holder.save()
    return card_holder


def _addCardToCardHolder(card_holder: CardHolder, card: CreditCardProduct):
    card_holder_card = CardHolderCard(card_holder=card_holder, card=card)
    card_holder_card.save()


def _removeCardFromCardHolder(card_holder: CardHolder, card: CreditCardProduct):
    card_holder_card = CardHolderCard.objects.get(card_holder=card_holder, card=card)
    card_holder_card.delete()

    
def _generate_card_statement(card_from_cardholder: CardHolderCard):
    statement = AccountStatement(card_from_cardholder=card_from_cardholder)
    statement.save()


def test_create_cardholder(request):
    user = _createUser({'name': 'joselito', 'email': 'joselito@gmail.com', 'password': '123456'})
    _saveUser(user)
    _createCardHolderForUser(user)
    return HttpResponse("Cardholder created successfully!")


def test_create_card(request):
    card = _createCreditCardProduct({'card_name': 'Visa', 'bank_name': 'Banco de Chile', 'interest_rate': 0.35, 'annuity': 22.00})
    _saveCreditCardProduct(card)
    return HttpResponse("Card created successfully!")


def test_add_card_to_cardholder(request):
    card_holder = CardHolder.objects.get(user='joselito@gmail.com')
    card = CreditCardProduct.objects.get(card_id=1)
    _addCardToCardHolder(card_holder, card)
    return HttpResponse("Cardholder card added successfully!")


def test_remove_card_from_cardholder(request):
    card_holder = CardHolder.objects.get(user='joselito@gmail.com')
    card = CreditCardProduct.objects.get(card_id=1)
    _removeCardFromCardHolder(card_holder, card)
    return HttpResponse("Cardholder card deleted successfully!")
    

def test_generate_card_statement(request):
    card_from_cardholder = CardHolderCard.objects.get(card_holder_cards_id=3)
    _generate_card_statement(card_from_cardholder)
    return HttpResponse("Card statement generated successfully!")
