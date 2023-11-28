from ..dao import CreditCardProductDao
from django.http import JsonResponse
from ..dao.CreditCardProductDao import CreditCardProductDao


class ViewGetAllCards():
    
    def render(self):
        cards = CreditCardProductDao().get_all()
        cards_json = list(cards.values())
        return JsonResponse(cards_json, safe=False)
