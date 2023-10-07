
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class ShortenerTests(APITestCase):

    def obtain_token(self):
        # create a test user
        user_data = {
            "email": "testuser@example.com",
            "password": "testpassword"
        }
        self.client.post(reverse('user-signup-list'), user_data, format='json')
        
        # obtain a token for the test user
        response = self.client.post(reverse('login'), user_data, format='json')
        return response.data['access']
    
    def setUp(self):
        self.token = self.obtain_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)


    def test_url_shortening(self):
        # test if link redirects to correct website
        url = reverse('my_shortener_namespace:create_api')
        data = {'original_link': 'https://www.example.com/long-url'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('shortened_link', response.data)

    def test_access_shortened_url(self):
        url = reverse('my_shortener_namespace:create_api')
        data = {'original_link': 'https://www.example.com/long-url'}
        shortened_response = self.client.post(url, data, format='json')
        shortened_link = shortened_response.data['shortened_link']
        
        # check redirection
        response = self.client.get(reverse('redirector', args=[shortened_link.split('/')[-1]]))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, data['original_link'])

    def test_existing_shortened_url(self):
        url = reverse('my_shortener_namespace:create_api')
        data = {'original_link': 'https://www.example.com/long-url'}
        
        # Create link for the first time
        response_first = self.client.post(url, data, format='json')
        shortened_link_first = response_first.data['shortened_link']

        # Create same link again
        response_second = self.client.post(url, data, format='json')
        shortened_link_second = response_second.data['shortened_link']

        # Test if they are the same
        self.assertEqual(shortened_link_first, shortened_link_second)

    def test_invalid_url(self):
        url = reverse('my_shortener_namespace:create_api')
        data = {'original_link': 'invalid-url'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('original_link', response.data)