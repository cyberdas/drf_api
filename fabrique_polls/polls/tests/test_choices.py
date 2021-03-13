from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

from .utils import create_choices


class ChoicesViewSetTest(APITestCase):

    def setUp(self):
        User = get_user_model()
        self.user_admin = User.objects.create_superuser(
            username="testadmin", password="testadmin")
        self.client.force_authenticate(user=self.user_admin)
        create_choices()

    def test_choices_list_admin(self):
        response = self.client.get(reverse(
            "choices-list", kwargs={"poll_id": 1, "question_id": 2}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_choices_list_user(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse(
            "choices-list", kwargs={"poll_id": 1, "question_id": 2}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_choices_admin(self):
        url = reverse("choices-list", kwargs={"poll_id": 1, "question_id": 2})
        data = {"text": "Новый выбор"}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_choices_detail_admin(self):
        response = self.client.get(reverse(
            "choices-detail", kwargs={"poll_id": 1, "question_id": 2, "pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_choices_admin(self):
        url = reverse(
            "choices-detail",
            kwargs={"poll_id": 1, "question_id": 2, "pk": 1})
        data = {
            "text": "Новый текст выбора"
        }
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
