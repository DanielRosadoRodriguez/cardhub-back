import json

from .dao.AccountStatementDao import AccountStatementDao
from .dao.UserDao import UserDao

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
            _createCardHolderForUser(newUser)
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
            cardholder_card_id = _addCardToCardHolder(card_holder, card)
        except json.JSONDecodeError as e:
            print("Error analyzing JSON: ", e)
        response = list([{"email": data["email"], "cardholder_card_id": cardholder_card_id}])
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
def create_cardholder_for_user_given_email(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = User.objects.get(email=data['email'])
            _createCardHolderForUser(user)
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
        user_email = data.get('email', '')
        
        try:
            card_holder = CardHolder.objects.get(user=user_email)
        except CardHolder.DoesNotExist:
            return JsonResponse([], safe=False)

        card_holder_cards = CardHolderCard.objects.filter(card_holder=card_holder)
        
        if not card_holder_cards.exists():
            return JsonResponse([], safe=False)

        cards = CreditCardProduct.objects.filter(cardholdercard__in=card_holder_cards)

        cards_data = [
            {
                'card_holder_card': model_to_dict(card_holder_card),
                'card': model_to_dict(card),
            }
            for card_holder_card, card in zip(card_holder_cards, cards)
        ]

        return JsonResponse(cards_data, safe=False)
    else:
        return HttpResponse("Invalid form submission method")


def _get_cardholder_statement(cardholder_card_id):
    statements = AccountStatement.objects.filter(card_from_cardholder=cardholder_card_id)
    statements_json = list(statements.values())
    return JsonResponse(statements_json, safe=False)


def _get_last_statement(cardholder_card_id):
    statement = AccountStatement.objects.filter(card_from_cardholder=cardholder_card_id).order_by('-statement_id')[0]
    statement_dict = model_to_dict(statement)
    return JsonResponse(statement_dict, safe=False)
    

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
    print("el id de la card es: " , card_holder_card.card_holder_cards_id)
    return card_holder_card.card_holder_cards_id



def _removeCardFromCardHolder(card_holder: CardHolder, card: CreditCardProduct):
    card_holder_card = CardHolderCard.objects.get(card_holder=card_holder, card=card)
    card_holder_card.delete()


def _add_website_to_card(card: CreditCardProduct, website_url: str, website_content: str):
    card_website = CardWebPage(page_url=website_url, page_content=website_content, associated_cards=card)
    card_website.save()


def test_create_cardholder(request):
    user = UserDao().build_user({'name': 'joselito', 'email': 'joselito@gmail.com', 'password': '123456'})
    UserDao().save(user)
    _createCardHolderForUser(user)
    return HttpResponse("Cardholder created successfully!")


def test_create_card(request):
    card = _createCreditCardProduct({'card_name': 'MasterCard', 'bank_name': 'Banamex', 'interest_rate': 10, 'annuity': 500})
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
    params = {
        'date': None,
        'cut_off_date': None,
        'payment_date': None,
        'current_debt': None,
        'pni': None,
        'card_from_cardholder': card_from_cardholder
    }
    statement = AccountStatementDao().build_card_statement(params)
    AccountStatementDao().save(statement)
    return HttpResponse("Card statement generated successfully!")


def test_add_website_to_card(request):
    card = CreditCardProduct.objects.get(card_id=1)
    _add_website_to_card(card, 'https://www.bancochile.cl', 'Banco de Chile')
    return HttpResponse("Website added to card successfully!")


def test_get_cardholder_statement(request):
    cardholder_card = CardHolderCard.objects.get(card_holder_cards_id=3)
    return _get_cardholder_statement(cardholder_card)


def test_get_last_statement(request):
    cardholder_card = CardHolderCard.objects.get(card_holder_cards_id=3)
    return _get_last_statement(cardholder_card)


def test_get_all_user_statements(request):
    email='joselito@gmail.com'
    return AccountStatementDao().get_all_user_statements(email)

