from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class ResumeSecurityTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="one", password="StrongPass123")
        self.user2 = User.objects.create_user(username="two", password="StrongPass123")
        token = str(RefreshToken.for_user(self.user1).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_resume_list_is_private(self):
        response = self.client.get("/api/resumes/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_register(self):
        response = self.client.post("/api/auth/register/", {
            "username":"three", "email":"three@example.com", "password":"StrongPass123"
        })
        self.assertEqual(response.status_code, 201)
