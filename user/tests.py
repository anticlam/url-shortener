from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class UserTests(APITestCase):

    def setUp(self):
        self.signup_url = reverse('user-signup-list')
        self.login_url = reverse('login')
        self.user_data = {'email': 'testuser@example.com', 'password': 'testpass123'}

        # Create a user 
        self.client.post(self.signup_url, self.user_data, format='json')

    def test_user_creation(self):
        data = {'email': 'newuser@example.com', 'password': 'newpass123'}
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('email', response.data['data'])

    def test_user_login(self):
        response = self.client.post(self.login_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_token_validation(self):
        # Get token
        login_response = self.client.post(self.login_url, self.user_data, format='json')
        token = login_response.data['access']

        # Test authentication 
        headers = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        response = self.client.get(reverse('user-signup-list'), **headers)
        
        # Make sure only admin has access
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # Test with bad token
        headers_invalid = {'HTTP_AUTHORIZATION': 'Bearer invalid_token'}
        response_invalid = self.client.get(reverse('user-signup-list'), **headers_invalid)
        self.assertEqual(response_invalid.status_code, status.HTTP_403_FORBIDDEN)