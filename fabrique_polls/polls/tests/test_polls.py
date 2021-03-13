from datetime import timedelta
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from .utils import create_poll


class PollsViewSetTest(APITestCase):   # в APITesTCase self.client = ApiClient(), есть force_authenticate

    url = reverse("polls-list")

    def setUp(self):
        User = get_user_model()
        self.user_admin = User.objects.create_superuser(
            username="testadmin", password="testadmin")
        self.client.force_authenticate(user=self.user_admin)
        create_poll()

    def test_polls_list_admin(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_polls_list_user(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_poll_admin(self):
        today = timezone.now() + timedelta(days=1)
        end = today + timedelta(days=3)
        data = {
            "title": "Тест", "start_date": today,
            "end_date": end, "description": "123"}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_change_poll_admin(self):
        data = {"title": "Новое название"}
        response = self.client.patch(
            reverse("polls-detail", kwargs={"pk": 1}), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Новое название", response.data["title"])

    def test_polls_detail_admin(self):
        response = self.client.get(reverse("polls-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_polls_detail_user(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse("polls-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
