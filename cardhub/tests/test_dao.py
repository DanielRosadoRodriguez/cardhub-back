from django.http import JsonResponse
from django.test import TransactionTestCase
from cardhub.dao.UserDao import UserDao
from cardhub.models import User

class TestUserDao(TransactionTestCase):
    
    def setUp(self):
        self.test_user: User = User(
            name='test',
            email='test@test.com',
            password='testpassword'
        )
    
    
    def test_save_user(self):

        expected_response:JsonResponse = JsonResponse({'status': 'success'})
        response:JsonResponse = UserDao().save(user=self.test_user)
        assert response.content == expected_response.content


