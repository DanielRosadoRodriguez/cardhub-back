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
    annuity = models.DecimalField(max_digits=5, decimal_places=2)
    
    
class CardHolder(models.Model):
    credit_card_products = models.ManyToManyField(CreditCardProduct)
  

class CardWebPage(models.Model):
    pageID = models.AutoField(primary_key=True)
    page_url = models.CharField(max_length=100)
    page_content = models.TextField()
    associated_cards = models.OneToManyField(CreditCardProduct)    

