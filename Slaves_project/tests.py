from django.urls import reverse
from django.test import Client, TestCase


class TestIndex(TestCase):
    def test_index_opens(self):
        c = Client()
        response = c.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_index_context(self):
        c = Client()
        response = c.get(reverse('index'))
        self.assertEqual(response.context, {})



class EnterTest(TestCase):
    def test_enter_opens(self):
        c = Client()
        response = c.get(reverse("enter"))

class LoginTest(TestCase):
    def test_login_opens(self):
        c = Client()
        response = c.get(reverse("login"))

        self.assertEqual(response.status_code, 200)

    def test_login_context(self):
        c = Client()
        response = c.get(reverse('login'))
        self.assertEqual(response.context, {})


class CatalogTest(TestCase):

    def test_catalog_opens(self):

    def test_login_opens(self):

        c = Client()
        response = c.get(reverse("catalog"))
        self.assertEqual(response.status_code, 200)


    def test_catalog_context(self):

    def test_login_context(self):

        c = Client()
        response = c.get(reverse('catalog'))
        self.assertEqual(response.context, {})


class RegistrationTest(TestCase):

    def test_registration_opens(self):

    def test_login_opens(self):

        c = Client()
        response = c.get(reverse("registration"))
        self.assertEqual(response.status_code, 200)


    def test_registration_context(self):
        c = Client()
        response = c.get(reverse('registration'))
        self.assertEqual(response.context, {})

"""class DataBaseTest(TestCase):
    def test_DataBase_creates(self):
        c = Client()"""

    def test_login_context(self):
        c = Client()
        response = c.get(reverse('registration'))
        self.assertEqual(response.context, {})

