from django.db import models

# Create your models here.

class User(models.Model):
    email = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    

class CreditCardProduct(models.Model):
    card_id = models.AutoField(primary_key=True)
    card_name = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    annuity = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    
class CardHolder(models.Model):
    card_holder_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class CardHolderCard(models.Model):
    card_holder_cards_id = models.AutoField(primary_key=True)
    card_holder = models.ForeignKey(CardHolder, on_delete=models.CASCADE)
    card = models.ForeignKey(CreditCardProduct, on_delete=models.CASCADE)


class CardWebPage(models.Model):
    pageID = models.AutoField(primary_key=True)
    page_url = models.CharField(max_length=100)
    page_content = models.TextField()
    associated_cards = models.ForeignKey(CreditCardProduct, on_delete=models.CASCADE)


class AccountStatement(models.Model):
    statement_id = models.AutoField(primary_key=True)
    date = models.DateField()
    cut_off_date = models.DateField()
    payment_date = models.DateField()
    current_debt = models.DecimalField(max_digits=10, decimal_places=2)
    payment_for_no_interest = models.DecimalField(max_digits=10, decimal_places=2)
    card = models.ForeignKey(CardHolderCard, on_delete=models.CASCADE)
