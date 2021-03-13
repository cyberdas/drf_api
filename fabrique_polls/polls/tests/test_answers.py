import json

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from .utils import create_choices


class AnswerTest(APITestCase):

    def setUp(self):
        self.user_id = 10
        create_choices()

    def test_text_answer(self):
        data = {"user_id": self.user_id, "question": 1, "text": "Ответ на вопрос"}
        wrong_data = {"user_id": self.user_id, "question": 2, "text": "Ответ на вопрос"}
        response = self.client.post(reverse("text_answer"), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(reverse("text_answer"), data=wrong_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Ответ должен быть на вопрос типа Text", response.data["question"])

    def test_choice_answer(self):
        data = {"user_id": self.user_id, "question": 2, "choice": 1}
        response = self.client.post(reverse("choice_answer"), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ActivePollsTest(APITestCase):

    def setUp(self):
        create_choices()

    def test_active_polls(self):
        response = self.client.get("/api/polls-active/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
