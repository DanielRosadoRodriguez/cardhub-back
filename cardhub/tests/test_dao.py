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
        self.user_dao: UserDao = UserDao()
    
    
    def test_save_user(self):
        expected_response:JsonResponse = JsonResponse({'status': 'success'})
        response:JsonResponse = self.user_dao.save(user=self.test_user)
        assert response.content == expected_response.content

    
    def test_get_user(self):
        expected_user = self.test_user
        self.user_dao.save(user=self.test_user)
        response_user: User = UserDao().get('test@test.com')
        assert response_user == expected_user

