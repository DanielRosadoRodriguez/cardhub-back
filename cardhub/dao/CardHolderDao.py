from .Dao import Dao
from cardhub.models import CardHolder 

class CardHolderDao(Dao):
    
    def get(self, id: int) -> CardHolder:
        try: 
            card_holder = CardHolder.objects.get(user=id)
            return card_holder
        except CardHolder.DoesNotExist:
            raise Exception(f'Card holder with id {id} was not found')
    
    def get_all(self) -> list[CardHolder]:
        try:
            card_holders = CardHolder.objects.all()
            return card_holders
        except CardHolder.DoesNotExist:
            raise Exception(f'No card holders were found')
    
    def save(self, card_holder: CardHolder) -> CardHolder:
        try:
            card_holder.save()
            return card_holder
        except Exception as e:
            raise Exception(f'Error saving card holder with id {card_holder.id}: {e}')
    
    def update(self, card_holder: CardHolder, data: dict) -> CardHolder:
        try:
            for key, value in data.items():
                setattr(card_holder, key, value)
                card_holder.save()
            return card_holder
        except Exception as e:
            raise Exception(f'Error updating card holder with id {card_holder.id}: {e}')
        
    def delete(self, card_holder: CardHolder) -> CardHolder:
        try:
            card_holder.delete()
            return card_holder
        except Exception as e:
            raise Exception(f'Error deleting card holder with id {card_holder.id}: {e}')
        