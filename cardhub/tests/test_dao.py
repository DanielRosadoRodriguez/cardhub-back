from django.test import SimpleTestCase
from cardhub.dao.UserDao import UserDao
from cardhub.models import User

class TestUserDao(SimpleTestCase):
    
    
    def test_get_user_by_email(self):
        expected_user: User = User(
            name='joselito',
            email='joselito@gmail.com',
            password='123456'
        )
        received_user = UserDao.get(email='joselito@gmail.com')
        assert expected_user == received_user