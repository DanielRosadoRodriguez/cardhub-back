from .app_views import ViewGenerateCardStatement
from .app_views import ViewGetAllUserCards
from .app_views import ViewRemoveCardFromCardholder
from .app_views import ViewGetLastStatement
from .app_views import ViewSignUp
from .app_views import ViewLogin
from .app_views import ViewGetAllCards
from .app_views import ViewAddCardToCardholder
from .app_views import ViewGetAllStatementsFromCard

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
