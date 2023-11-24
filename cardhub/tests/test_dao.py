from django.http import JsonResponse
from django.test import TransactionTestCase
from cardhub.dao.UserDao import UserDao
from cardhub.models import User

class TestUserDao(TransactionTestCase):
    
    def test_create_user(self):
        user: User = User(
            name='test',
            email='test@test.com',
            password='testpassword'
        )
        expected_response:JsonResponse = JsonResponse({'status': 'success'})
        response:JsonResponse = UserDao.save(user)
        assert response.content == expected_response.content
