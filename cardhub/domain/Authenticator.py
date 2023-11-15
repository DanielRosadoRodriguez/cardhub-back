from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from ..models import User

class Authenticator:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def authenticate_user(self):
        try:
            user = User.objects.get(email=self.email)
            if user.password == self.password:
                return True
        except User.DoesNotExist:
            print("User does not exist") 

        return False