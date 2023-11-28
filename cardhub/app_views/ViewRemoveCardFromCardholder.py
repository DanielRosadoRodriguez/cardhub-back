import json

from ..dao import CreditCardProductDao
from ..dao import CardHolderDao

from django.http import JsonResponse


class GetAllUserCards():
        
    def __init__(self, request):
        self.request = request
        self.data = json.loads(request.body)
        self.card_id = self.data['card_id']
        self.email = self.data['email']



    def render(self):
        if self.is_post_method(self):
            return self.build_response()
        else:
            return JsonResponse([self.error_message], safe=False)
    

    def _is_post_method(self):
        return self.request.method == "POST"
    

    def _build_response(self):
        cardholder = CardHolderDao().get(self.email)
        card = CreditCardProductDao().get(self.card_id)
        deleted = cardholder.remove_card(card)
        return JsonResponse(list(deleted), safe=False)
