import json
from cardhub.domain.Authenticator import Authenticator
from django.http import JsonResponse


class ViewLogin():
    
    def __init__(self, request):
        self.data = json.loads(request.body)
        self.request = request
        self.email = self.data['email']
        self.password = self.data['password']
        self.error_message = "Invalid form submission method"
    
    
    def render(self):
        if self.request.method == "POST":
            return self.build_response()
        else:
            return JsonResponse([self.error_message], safe=False)
    
    def build_response(self):
        authenticator = Authenticator(self.email, self.password)
        is_authenticated = authenticator.authenticate_user()
        response_data = {"authenticated": str(is_authenticated)} 
        response_data_json = list(response_data.values())
        return JsonResponse(response_data_json, safe=False)
