from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserModel

class UserListViewTest(TestCase):

    def setUp(self):
        """Cria um usuário para testes antes de cada teste"""
        user_obj = User.objects.create_user(username='testuser', password='password')
        self.user = user_obj
        self.user_model = UserModel.objects.create(
            user=user_obj,
            name="Test User",
            cnpj="12345678000195",
            email="testuser@example.com",
            password="password"  # A senha é criptografada no método save()
        )

    def test_user_list_view_status_code(self):
        """Testa se a página user_list.html é renderizada corretamente"""
        # Simula um login antes de acessar a página
        self.client.login(username='testuser', password='password')
        url = reverse('user_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_user_list_view_template(self):
        """Verifica se o template user_list.html é utilizado"""
        # Simula um login antes de acessar a página
        self.client.login(username='testuser', password='password')
        url = reverse('user_list')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'user/user_list.html')

    def test_user_list_view_context(self):
        """Verifica se o contexto da view contém os usuários esperados"""
        # Simula um login antes de acessar a página
        self.client.login(username='testuser', password='password')
        url = reverse('user_list')
        response = self.client.get(url)
        self.assertIn('users', response.context)
        self.assertEqual(len(response.context['users']), 1)
        self.assertEqual(response.context['users'][0].name, "Test User")
    