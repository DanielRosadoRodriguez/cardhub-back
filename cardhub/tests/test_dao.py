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
        self.test_users: list[User] = self._build_test_users()
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


    def test_get_all_users(self):
        expected_users = self.test_users
        self._save_every_user(users=expected_users)
        response_users: list[User] = self.user_dao.get_all()
        assert response_users == expected_users

        
    def _build_test_users(self):
        return [ 
            User(
                name=f'test{i}',
                email=f'test{i}@test.com',
                password=f'testpassword{i}'
            )
            for i in range(1, 4)
        ]


    def _save_every_user(self, users: list[User]):
        for user in users:
            self.user_dao.save(user=user)