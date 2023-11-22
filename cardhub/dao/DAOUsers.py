from django.http import JsonResponse
from cardhub.models import User


def save_user(user: User) -> JsonResponse:
    user.save()
    return JsonResponse({'status': 'success'})


def get_user_by_email(email: str) -> User:
    return User.objects.get(email=email)


def get_all_users() -> JsonResponse:
    users = User.objects.all()
    return users
