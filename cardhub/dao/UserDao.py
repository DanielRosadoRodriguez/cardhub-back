from django.http import JsonResponse
from cardhub.models import User
from .Dao import Dao

class UserDao(Dao):

    def get(email: str) -> User:
        return User.objects.get(email=email)


    def get_all() -> list[User]:
        users = User.objects.all()
        return users


    def save(user: User) -> JsonResponse:
        user.save()
        return JsonResponse({'status': 'success'})


    def update(user: User, params: dict) -> JsonResponse:
        user = User(
            name=params['name'],
            email=params['email'],
            password=params['password']
        )
        user.save()
        return JsonResponse({'status': 'success'})


    def delete(user: User) -> JsonResponse:
        user.delete()
        return JsonResponse({'status': 'success'})
