import json

from .app_views import ViewGenerateCardStatement
from .app_views import ViewGetAllUserCards
from .app_views import ViewRemoveCardFromCardholder

from .app_views import ViewGetLastStatement
from .app_views import ViewSignUp
from .app_views.ViewLogin import ViewLogin
from .app_views.ViewGetAllCards import ViewGetAllCards
from .app_views.ViewAddCardToCardholder import ViewAddCardToCardholder
from .app_views.ViewGetAllStatementsFromCard import ViewGetAllStatementsFromCard

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
    return ViewSignUp(request).render()
    

@csrf_exempt
def login(request):
    return ViewLogin(request).render()


@csrf_exempt
def add_card_to_user_cardholder(request):
    return ViewAddCardToCardholder(request).render()

        
@csrf_exempt
def remove_card_from_cardholder(request):
    return ViewRemoveCardFromCardholder(request).render()


@csrf_exempt
def generate_card_statement(request):
    return ViewGenerateCardStatement(request).render()


@csrf_exempt
def get_all_cards(request):
    return ViewGetAllCards().render()


@csrf_exempt
def get_all_user_cards(request):
    return ViewGetAllUserCards(request).render()


@csrf_exempt
def get_last_statement(request):
    return ViewGetLastStatement(request).render()


@csrf_exempt
def get_all_statement_from_card(request):
    return ViewGetAllStatementsFromCard(request).render()
