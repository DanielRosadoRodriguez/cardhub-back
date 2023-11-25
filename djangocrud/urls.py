"""
URL configuration for djangocrud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from cardhub import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login, name='log_in_form'),
    path('signup/', views.signup, name='sign_up_form'),
    path('test_create_cardholder/', views.test_create_cardholder, name='test_create_cardholder'),
    path('test_create_card/', views.test_create_card, name='test_create_card'),
    path('test_add_card_to_cardholder/', views.test_add_card_to_cardholder, name='test_add_card_to_cardholder'),
    path('add_card_to_user_cardholder/', views.add_card_to_user_cardholder, name='add_card_to_user_cardholder'),
    path('get_all_cards/', views.get_all_cards, name='get_all_cards'),
    path('test_remove_card_from_cardholder/', views.test_remove_card_from_cardholder, name='test_remove_card_from_cardholder'),
    path('remove_card_from_user_cardholder/', views.remove_card_from_user_cardholder, name='remove_card_from_user_cardholder'),
    path('generate_card_statement/', views.generate_statement_w_params, name='test_generate_card_statement'),
    path('generate_card_statement/', views.generate_card_statement, name='generate_card_statement'),
    path('test_add_website_to_card/', views.test_add_website_to_card, name='test_add_website_to_card'),
    path('test_get_cardholder_statement/', views.test_get_cardholder_statement, name='test_get_cardholder_statement'),
    path('get_all_user_cards/', views.get_all_user_cards, name='test_get_all_user_cards'),
    path('test_get_last_statement/', views.test_get_last_statement, name='test_get_last_statement'),
    path('create_cardholder_for_user_given_email/', views.create_cardholder_for_user_given_email, name='create_cardholder_for_user_given_email'),
    path('test_get_stetement_w_all_params/', views.test_get_stetement_w_all_params, name='test_get_stetement_w_all_params'),
    path('test_get_all_user_statements/', views.test_get_all_user_statements, name='test_get_all_user_statements'),
    path('test_create_statement_w_some_params/', views.test_create_statement_w_some_params, name='test_create_statement_w_some_params'),
    path('test_create_statement_without_params/', views.test_create_statement_without_params, name='test_create_statement_without_params'),

]
