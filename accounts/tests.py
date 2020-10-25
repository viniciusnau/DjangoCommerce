from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase


User = get_user_model()


class UserTestCast(TestCase):
    
    def setUp(self):
        user = User(username='cfe', email='cfe@invalid.com')
        user_pw = 'some_123_password'
        self.user_pw = user_pw
        user.is_staff = True
        user.is_superuser = True
        user.set_password(user_pw)
        user.save()
        self.user = user

    def test_user_exists(self):
        user_count = User.objects.all().count()
        self.assertEqual(user_count, 1)
        self.assertNotEqual(user_count, 0)

    def test_user_password(self):
        user = User.objects.get(username="cfe")
        self.assertTrue(user.check_password(self.user_pw))

    def test_login_url(self):
        login_url = settings.LOGIN_URL
        data = {"username":"cfe", "password": self.user_pw}
        response = self.client.post(login_url, data, follow=True)
        status_code = response.status_code
        redirect_path = response.request.get("PATH_INFO")
        # self.assertEqual(redirect_path, settings.LOGIN_REDIRECT_URL)
        self.assertEqual(status_code, 200)
    