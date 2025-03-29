from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserModel
from rest_framework.test import APIClient
from rest_framework import status


class UserModelViewSetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpassword")
        self.client = APIClient()
        self.client.login(username="testuser", password="testpassword")
        self.user_model = UserModel.objects.create(user=self.user, name="Test User", cnpj="12345678000195", email="test@example.com", password="testpassword")
    
    def test_user_model_viewset_list(self):
        """Test if the user can view their profile using the API"""
        response = self.client.get(reverse('usermodel-list'))  # Use the correct name for your viewset URL
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one user should exist in the DB

    def test_user_model_viewset_create(self):
        """Test if the user can create a new profile"""
        data = {
            "user": self.user.id,
            "name": "New User",
            "cnpj": "12345678000196",
            "email": "new@example.com",
            "password": "newpassword"
        }
        response = self.client.post(reverse('usermodel-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_model_viewset_update(self):
        """Test if the user can update their profile"""
        data = {
            "name": "Updated User",
            "cnpj": "12345678000197",
            "email": "updated@example.com",
            "password": "updatedpassword"
        }
        response = self.client.put(reverse('usermodel-detail', kwargs={'pk': self.user_model.pk}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user_model.refresh_from_db()
        self.assertEqual(self.user_model.name, "Updated User")

    def test_user_model_viewset_delete(self):
        """Test if the user can delete their profile"""
        response = self.client.delete(reverse('usermodel-detail', kwargs={'pk': self.user_model.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(UserModel.objects.filter(pk=self.user_model.pk).exists())


class UserViewsTestCase(TestCase):
    def setUp(self):
        # Criação de um usuário válido para o teste de login
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpassword")
        self.user_model = UserModel.objects.create(user=self.user, name="Test User", cnpj="12345678000195", email="test@example.com", password="testpassword")

    def test_user_login(self):
        """Test login functionality"""
        response = self.client.post(reverse('user_login'), {'email': 'test@example.com', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)  # Espera redirecionamento para user_list após login
        self.assertRedirects(response, reverse('user_list'))

    def test_user_logout(self):
        """Test logout functionality"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('user_logout'))
        self.assertEqual(response.status_code, 302)  # Espera redirecionamento para login após logout
        self.assertRedirects(response, reverse('user_login'))

    def test_user_create(self):
        """Test profile creation functionality"""
        response = self.client.post(reverse('user_create'), {'name': 'New User', 'cnpj': '12345678000196', 'email': 'new@example.com', 'password': 'newpassword'})
        self.assertEqual(response.status_code, 302)  # Redirect to user list after creating the profile
        self.assertRedirects(response, reverse('user_login'))

    def test_user_update(self):
        """Test if the user can update their profile"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('user_update', kwargs={'pk': self.user_model.id}), {
            'name': 'Updated User',
            'cnpj': '12345678000197',
            'email': 'updated@example.com',
            'password': 'updatedpassword'
        })
        self.assertEqual(response.status_code, 302)  # Espera redirecionamento após atualização
        self.assertRedirects(response, reverse('user_list'))

    def test_user_delete(self):
        """Test profile deletion functionality"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('user_delete', kwargs={'pk': self.user_model.id}))
        self.assertEqual(response.status_code, 302)  # Espera redirecionamento após exclusão
        self.assertRedirects(response, reverse('user_login'))  # Espera redirecionamento para user_list
        self.assertFalse(UserModel.objects.filter(user=self.user).exists())  # Certifica que o perfil foi excluído
