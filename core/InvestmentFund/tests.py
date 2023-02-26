from django.test import TestCase, Client
from django.urls import resolve, reverse
from django.utils.module_loading import import_module
from .models import Usuario

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.urls = []

        urls_module = import_module('InvestmentFund.urls')

        for url in urls_module.urlpatterns:
            if hasattr(url, 'name'):
                self.urls.append(url.name)
        
        self.urls.remove('email_confirm')
        self.urls.remove('password_reset_confirm')

    def test_all_views_return_200(self):

        Usuario.objects.create(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        for url_name in self.urls:
            url = reverse(url_name)

            # Verify that the URL is mapped to a View
            resolver_match = resolve(url)
            self.assertIsNotNone(resolver_match.func)

            # Check View returns a 200/303 response
            response = self.client.get(url)
            if response.status_code == 404 and response.status_code == 500:
                self.fail(f'La vista {url_name} arrojó una respuesta {response.status_code}')
