from django.test import SimpleTestCase
from django.urls import reverse,resolve
from home.views import home_view
from register.views import login, signup, logout
from dashboard.views import user_dashboard, mech_dashboard, employee_dashboard, mechanic_booking, employee_earnings, mech_earnings,user_took, user_gib, mech_details, car_details, mech_checkout_view, checkout_view, success_payment
class TestUrls(SimpleTestCase):

    def test_home_url_is_resolved(self):
        url = reverse('home')
        print(resolve(url))
        self.assertEquals(resolve(url).func, home_view)

    def test_login_url_is_resolved(self):
        url = reverse('login')
        print(resolve(url))
        self.assertEquals(resolve(url).func, login)

    def test_signup_url_is_resolved(self):
        url = reverse('signup')
        print(resolve(url))
        self.assertEquals(resolve(url).func, signup)

    def test_logout_url_is_resolved(self):
        url = reverse('logout')
        print(resolve(url))
        self.assertEquals(resolve(url).func, logout)

    def test_user_dashboard_url_is_resolved(self):
        url = reverse('user_dashboard')
        print(resolve(url))
        self.assertEquals(resolve(url).func, user_dashboard)

    def test_mechanic_booking_url_is_resolved(self):
        url = reverse('mechanic_booking')
        print(resolve(url))
        self.assertEquals(resolve(url).func, mechanic_booking)

    def test_emp_dashboard_url_is_resolved(self):
        url = reverse('emp_dashboard')
        print(resolve(url))
        self.assertEquals(resolve(url).func, employee_dashboard)
    

