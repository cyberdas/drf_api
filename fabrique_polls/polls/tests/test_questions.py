from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

from .utils import create_questions


class QuestionsViewSetTest(APITestCase):

    def setUp(self):
        User = get_user_model()
        self.user_admin = User.objects.create_superuser(
            username="testadmin", password="testadmin"
        )
        self.client.force_authenticate(user=self.user_admin)
        create_questions()

    def test_questions_list_admin(self):
        response = self.client.get(reverse(
            "questions-list", kwargs={"poll_id": 1}))
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_questions_list_user(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse(
            "questions-list", kwargs={"poll_id": 1})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_questions_admin(self):
        data = {
            "text": "Новый вопрос", "question_type": "Text"
        }
        response = self.client.post(
            reverse(
                "questions-list",
                kwargs={"poll_id": 1}), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_questions_detail_admin(self):
        url = reverse("questions-detail", kwargs={"poll_id": 1, "pk": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_questions_admin(self):
        url = reverse("questions-detail", kwargs={"poll_id": 1, "pk": 3})
        data = {
            "text": "Новый текст вопроса",
            "question_type": "Multichoice"
        }
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
