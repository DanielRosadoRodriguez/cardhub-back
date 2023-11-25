from django.http import JsonResponse
from cardhub.models import AccountStatement 
from .Dao import Dao

class AccountStatementDao(Dao):

    def get(self, id: int) -> AccountStatement:
        return AccountStatement.objects.get(id=id)


    def get_all(self) -> list[AccountStatement]:
        card_statements = list(AccountStatement.objects.all())
        return card_statements


    def save(self, card_statement: AccountStatement) -> JsonResponse:
        try:
            card_statement.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': e})


    def update(self, card_statement: AccountStatement, params: dict) -> JsonResponse:
        try:
            card_statement = self.build_card_statement(params) 
            card_statement.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': e})


    def delete(self, card_statement: AccountStatement) -> JsonResponse:
        try: 
            card_statement.delete()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': e})


    def build_card_statement(self, params: dict) -> AccountStatement:
        return AccountStatement(
            statement_id = params.get('statement_id'),
            date = params.get('date'),
            cut_off_date = params.get('cut_off_date'),
            payment_date = params.get('payment_date'),
            current_debt = params.get('current_debt'),
            payment_for_no_interest = params.get('pni'),
            card_from_cardholder = params.get('card_from_cardholder')
        )

