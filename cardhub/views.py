import json

from .dao.CardHolderDao import CardHolderDao
from .dao.AccountStatementDao import AccountStatementDao
from .dao.UserDao import UserDao
from .dao.CreditCardProductDao import CreditCardProductDao
from .dao.CardWebPageDao import CardWebpageDao

from django.forms import model_to_dict

from cardhub.domain.Authenticator import Authenticator
from django.core.serializers import serialize
from .models import CardWebPage, User
from .models import CardHolderCard
from .models import CardHolder
from .models import CreditCardProduct
from .models import AccountStatement
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            newUser: User = UserDao().build_user(data)
            UserDao().save(newUser)
            card_holder = CardHolder(user=newUser)
            CardHolderDao().save(card_holder)
            response_data = {"signed": True}
            return JsonResponse([str(response_data["signed"])], safe=False)
        except json.JSONDecodeError as e:
            return JsonResponse(["False"], safe=False)
    else:
        return HttpResponse("Invalid form submission method")
    

@csrf_exempt
def login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data['email']
            password = data['password']
            authenticator = Authenticator(email, password)
            is_authenticated = authenticator.authenticate_user()
            response_data = {"authenticated": str(is_authenticated)}  # Convierte a cadena para JSON
            response_data_json = list(response_data.values())
            return JsonResponse(response_data_json, safe=False)
        except json.JSONDecodeError as e:
            print("Error analyzing JSON: ", e)  
        return HttpResponse(is_authenticated)
    else:
        return HttpResponse("Invalid form submission method")


@csrf_exempt
def add_card_to_user_cardholder(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            card_holder = CardHolder.objects.get(user=data['email'])
            card = CreditCardProduct.objects.get(card_id=data['card_id'])
            card_holder_card = card_holder.add_card(card)
        except json.JSONDecodeError as e:
            print("Error analyzing JSON: ", e)
        response = list([{"email": data["email"], "cardholder_card_id": card_holder_card.id}])
        return JsonResponse(response, safe=False)
    else:
        return HttpResponse("Invalid form submission method")

    
@csrf_exempt
def remove_card_from_user_cardholder(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            card_holder = CardHolder.objects.get(user=data['email'])
            card_to_delete = CreditCardProduct.objects.get(card_id=data['card_id'])
            card_holder.remove_card(card_to_delete)
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
            params = {
                'date': data['date'],
                'cut_off_date': data['cut_off_date'],
                'payment_date': data['payment_date'],
                'current_debt': data['current_debt'],
                'pni': data['pni'],
                'card_from_cardholder': card_from_cardholder
            }
            statement = AccountStatementDao().build_card_statement(params)
            AccountStatementDao().save(statement)
        except json.JSONDecodeError as e:
            print("Error analyzing JSON: ", e)
        return HttpResponse("Form submitted successfully!")
    else:
        return HttpResponse("Invalid form submission method")


@csrf_exempt
def generate_statement_w_params(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data['card_holder_cards_id'])
            card_from_cardholder = CardHolderCard.objects.get(card_holder_cards_id=data['card_holder_cards_id'])
            params = {
                'date': data['date'],
                'cut_off_date': data['cut_off_date'],
                'payment_date': data['payment_date'],
                'current_debt': data['current_debt'],
                'pni': data['pni'],
                'card_from_cardholder': card_from_cardholder
            }
            statement = AccountStatementDao().build_card_statement(params)
            AccountStatementDao().save(statement)

            response_data = {
                'statement_id': statement.statement_id,
                'date': statement.date,
                'cut_off_date': statement.cut_off_date,
                'payment_date': statement.payment_date,
                'current_debt': statement.current_debt,
                'payment_for_no_interest': statement.payment_for_no_interest,
                'card_from_cardholder': statement.card_from_cardholder.card_holder_cards_id
            }
            response = list([response_data])
            return JsonResponse(response, safe=False)
        except json.JSONDecodeError as e:
            print("Error analyzing JSON: ", e)
            return HttpResponse("Invalid JSON data")
        except CardHolderCard.DoesNotExist:
            return HttpResponse("CardHolderCard not found for the specified card_holder_cards_id")
    else:
        return HttpResponse("Invalid form submission method")
    

@csrf_exempt
def create_cardholder_for_user_given_email(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = User.objects.get(email=data['email'])
            card_holder = CardHolder(user=user)
            CardHolderDao().save(card_holder)
        except json.JSONDecodeError as e:
            print("Error analyzing JSON: ", e)
        return HttpResponse("Form submitted successfully!")
    else:
        return HttpResponse("Invalid form submission method")


@csrf_exempt
def get_all_cards(request):
    cards = CreditCardProduct.objects.all()
    cards_json = list(cards.values())
    return JsonResponse(cards_json, safe=False)


@csrf_exempt
def get_all_user_cards(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        cardholder = CardHolder.objects.get(user=data['email'])
        cards = cardholder.get_cards()
        cards_data = list(cards.values())
        return JsonResponse(cards_data, safe=False)
    else:
        return HttpResponse("Invalid form submission method")


@csrf_exempt
def get_last_statement(request):
    if request.method == 'POST':
        try: 
            data = json.loads(request.body)
            cardholder_card_id = data['cardholder_card_id']
            statement = AccountStatementDao().get_last_card_statement(cardholder_card_id)
            return statement
        except json.JSONDecodeError as e:
            print("Error analyzing JSON: ", e)
            return HttpResponse("Invalid JSON data")
    else:
        return HttpResponse("Invalid form submission method")


@csrf_exempt
def remove_card_from_cardholder(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cardholder = CardHolderDao().get(data['cardholder_id'])
            card = CreditCardProductDao().get(data['card_id'])
            cardholder.remove_card(card)
            return HttpResponse("Card removed successfully")
        except json.JSONDecodeError as e:
            print("Error analyzing JSON: ", e)
            return HttpResponse("Invalid JSON data")
        except CardHolderCard.DoesNotExist:
            return HttpResponse("CardHolderCard not found for the specified cardholder_id")
    else:
        return HttpResponse("Invalid form submission method")
