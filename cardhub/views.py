from .app_views.ViewGenerateCardStatement import ViewGenerateCardStatement
from .app_views.ViewGetAllUserCards import GetAllUserCards
from .app_views.ViewRemoveCardFromCardholder import RemoveCardFromCardholder
from .app_views.ViewGetLastStatement import GetLastStatement
from .app_views.ViewSignUp import ViewSignUp
from .app_views.ViewLogin import ViewLogin
from .app_views.ViewGetAllCards import ViewGetAllCards
from .app_views.ViewAddCardToCardholder import ViewAddCardToCardholder
from .app_views.ViewGetAllStatementsFromCard import ViewGetAllStatementsFromCard



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
    return RemoveCardFromCardholder(request).render()


@csrf_exempt
def generate_card_statement(request):
    return ViewGenerateCardStatement(request).render()


@csrf_exempt
def get_all_cards(request):
    return ViewGetAllCards().render()


@csrf_exempt
def get_all_user_cards(request):
    return GetAllUserCards(request).render()


@csrf_exempt
def get_last_statement(request):
    return GetLastStatement(request).render()


@csrf_exempt
def get_all_statement_from_card(request):
    return ViewGetAllStatementsFromCard(request).render()
