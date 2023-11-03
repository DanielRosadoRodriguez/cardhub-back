from django.db import models

# Create your models here.

class UserWithWallet(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=100)
    
    
class CreditCardProduct(models.Model):
    card_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    associated_bank = models.CharField(max_length=100)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    
    
class CardHolder(models.Model):
    credit_card_products = models.ManyToManyField(CreditCardProduct)
  