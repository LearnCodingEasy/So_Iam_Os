from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class CoreHealthTests(APITestCase):

    def test_core_health_endpoint(self):
        url = reverse("core:health")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["status"],
            "success",
        )

        self.assertEqual(
            response.data["service"],
            "core",
        )
