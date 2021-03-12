from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

from .utils import create_questions, create_choices


class ChoicesViewSetTest(APITestCase):

    def setUP(self):
        User = get_user_model()
        self.user_admin = User.objects.create_superuser(
            username="testadmin", password="testadmin")
        self.client.force_authenticate(user=self.user_admin)
        create_choices()

    def test_choices_list_admin(self):
        response = self.client.get(reverse(
            "choices-list", kwargs={"poll_id": 1, "question_id": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_choices_list_user(self):
        pass

    def test_create_choices_admin(self):
        pass

    def test_choices_detail_admin(self):
        pass

    def test_change_choices_admin(self):
        pass
