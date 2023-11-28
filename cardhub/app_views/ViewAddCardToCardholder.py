import json

from ..dao.CardHolderDao import CardHolderDao
from ..dao.CreditCardProductDao import CreditCardProductDao
from django.http import JsonResponse


class ViewAddCardToCardholder():
    
    def __init__(self, request):
        self.request = request
        self.data = json.loads(request.body)
        self.email = self.data['email']
        self.card_id = self.data['card_id']


    def render(self):
        if self.is_post_method(self):
            return self.build_response()
        else:
            return JsonResponse([self.error_message], safe=False)
    

    def _is_post_method(self):
        return self.request.method == "POST"
    

    def _build_response(self):
        card_holder = CardHolderDao().get(self.email) 
        card = CreditCardProductDao().get(self.card_id)
        card_holder_card = card_holder.add_card(card)
        return list([{"email": self.email, "cardholder_card_id": card_holder_card.card_holder_cards_id}])