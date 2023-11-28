from ..dao import CreditCardProductDao
from django.http import JsonResponse


class ViewGetAllCards():
    
    def render(self):
        cards = CreditCardProductDao().get_all()
        cards_json = list(cards.values())
        return JsonResponse(cards_json, safe=False)
