from django.test import TestCase, Client
from django.urls import reverse
import json

class TestViews(TestCase):
    def test_home_view_GET(self):
        client = Client()

        response = client.get(reverse('home'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/home.html')

    def test_login_view_GET(self):
        client = Client()

        response = client.get(reverse('login'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'register/login.html')

    def test_signup_view_GET(self):
        client = Client()

        response = client.get(reverse('signup'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'register/signup.html')

    # def test_dashboard_view_GET(self):
    #     client = Client()

    #     response = client.get(reverse('user_dashboard'))

    #     self.assertEquals(response.status_code,200)
    #     self.assertTemplateUsed(response, 'dashboard/user.html')

