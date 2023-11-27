import json

from .app_views.ViewLogin import ViewLogin
from .app_views.ViewGetAllCards import ViewGetAllCards

from .dao.CardHolderDao import CardHolderDao
from .dao.AccountStatementDao import AccountStatementDao
from .dao.UserDao import UserDao
from .dao.CreditCardProductDao import CreditCardProductDao

from django.forms import model_to_dict

from .models import User
from .models import CardHolderCard
from .models import CardHolder
from .models import CreditCardProduct
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
    return ViewLogin(request).render()

@csrf_exempt
def add_card_to_user_cardholder(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            card_holder = CardHolderDao().get(data['email']) 
            card = CreditCardProductDao().get(data['card_id'])
            card_holder_card = card_holder.add_card(card)
            print(card_holder_card.card_holder_cards_id)
        except json.JSONDecodeError as e:
            print("Error analyzing JSON: ", e)
        response = list([{"email": data["email"], "cardholder_card_id": card_holder_card.card_holder_cards_id}])
        return JsonResponse(response, safe=False)
    else:
        return HttpResponse("Invalid form submission method")
    
        
@csrf_exempt
def remove_card_from_cardholder(request):
    if request.method == 'POST':
        try:
            
            data = json.loads(request.body)
            cardholder = CardHolderDao().get(data['email'])
            card = CreditCardProductDao().get(data['card_id'])
            
            deleted = cardholder.remove_card(card)
            return JsonResponse(list(deleted), safe=False)
        except json.JSONDecodeError as e:
            message = f"Error analyzing JSON: {e}"
            print(message)
            return JsonResponse([message], safe=False)
        except CardHolderCard.DoesNotExist:
            message = f"CardHolderCard not found for the specified email and card_id"
            return JsonResponse([message], safe=False)
    else:
        return JsonResponse(["Invalid form submission method"], safe=False)


# TODO - Pasar a DAO
@csrf_exempt
def generate_card_statement(request):
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
def get_all_cards(request):
    return ViewGetAllCards().render()


from .app_views.ViewGetAllCards import ViewGetAllCards
# TODO - Pasar a DAO
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
def get_all_statement_from_card(request):
    if request.method == 'POST':
        try: 
            data = json.loads(request.body)
            cardholder_card_id = data['cardholder_card_id']
            statement = AccountStatementDao().get_cardholder_statements(cardholder_card_id)
            return statement
        except json.JSONDecodeError as e:
            print("Error analyzing JSON: ", e)
            return HttpResponse("Invalid JSON data")
    else:
        return HttpResponse("Invalid form submission method")
