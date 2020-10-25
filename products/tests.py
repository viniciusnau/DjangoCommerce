from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Product

User = get_user_model()


class ProductTestCase(TestCase):

    def setUp(self):
        user = User(username='cfe', email='cfe@invalid.com')
        user_pw = 'some_123_password'
        self.user_pw = user_pw
        user.is_staff = True
        user.is_superuser = False
        user.set_password(user_pw)
        user.save()
        self.user = user
        user1 = User.objects.create_user('user1', 'cfe1@invalid.com', 'some_123_password')
        self.user1 = user1

    def test_user_count(self):
        user_count = User.objects.all().count()
        self.assertEqual(user_count, 2)

    def test_invalid_requst(self):
        self.client.login(username=self.user1.username, password='some_123_password')
        response = self.client.post("/products/create", {"title": "this is an invalid test"})
        self.assertNotEqual(response.status_code, 200)

    def test_valid_requst(self):
        self.client.login(username=self.user.username, password='some_123_password')
        response = self.client.post("/products/create/", {"title": "this is an valid test"})
        self.assertEqual(response.status_code, 200)