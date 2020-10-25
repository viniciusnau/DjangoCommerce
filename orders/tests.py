from django.test import TestCase

# Create your tests here.
class OrderTestCase(TestCase):
    
    def setUp(self):
        user = User(username='cfe', email='cfe@invalid.com')
        user_pw = 'some_123_password'
        self.user_pw = user_pw
        user.is_staff = True
        user.is_superuser = True
        user.set_password(user_pw)
        user.save()
        self.user = user

    def test_create_order(self):
        obj = Order.objects.create(user=self.user, product=product)