from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from shortener.models import Link
from user.models import User


class LinkTests(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser("admin@example.com", "password")
        self.client.login(email="admin@example.com", password="password")

    def test_create_shortened_link(self):
        url = reverse("my_shortener_namespace:create_api")
        data = {"original_link": "https://www.example.com"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Link.objects.count(), 1)
        self.assertEqual(Link.objects.get().original_link, "https://www.example.com")

    def test_list_shortened_links(self):
        Link.objects.create(original_link="https://www.example1.com")
        Link.objects.create(original_link="https://www.example2.com")
        url = reverse("my_shortener_namespace:all_links")
        response = self.client.get(url)
        print(f"Debug: Response Data in test_list_shortened_links: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data["results"]), 2
        )  

    def test_redirect_link_not_found(self):
        url = reverse("redirector", args=["nonexistent"])
        response = self.client.get(url)
        print(f"Debug: Response in test_redirect_link_not_found: {response.__dict__}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
