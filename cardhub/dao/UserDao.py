from django.http import JsonResponse
from cardhub.models import User
from .Dao import Dao

class UserDao(Dao):

    def get(self, email: str) -> User:
        return User.objects.get(email=email)


    def get_all(self) -> list[User]:
        users = list(User.objects.all())
        return users


    def save(self, user: User) -> JsonResponse:
        user.save()
        return JsonResponse({'status': 'success'})


    def update(self, user: User, params: dict) -> JsonResponse:
        user = User(
            name=params['name'],
            email=params['email'],
            password=params['password']
        )
        user.save()
        return JsonResponse({'status': 'success'})


    def delete(self, user: User) -> JsonResponse:
        user.delete()
        return JsonResponse({'status': 'success'})
