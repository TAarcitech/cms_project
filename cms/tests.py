from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from cms.models import User, Content
from rest_framework.authtoken.models import Token


class UserAuthTests(APITestCase):

    def test_user_registration_validation(self):
        data = {
            "username": "author",
            "email": "author@example.com",
            "password": "testpass",  # Invalid: no uppercase
            "first_name": "John",
            "last_name": "Doe",
            "role": "author",
            "phone": "1234567890",
            "pincode": "123456"
        }
        response = self.client.post("/api/register/", data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Password must contain both upper and lower case characters.", str(response.data))

    def test_duplicate_email_or_username(self):
        User.objects.create_user(
            username="author",
            email="author@example.com",
            password="TestPass123",
            role="author",
            phone="1234567890",
            pincode="123456"
        )
        data = {
            "username": "author",  # duplicate
            "email": "author@example.com",  # duplicate
            "password": "TestPass123",
            "first_name": "John",
            "last_name": "Doe",
            "role": "author",
            "phone": "1234567890",
            "pincode": "123456"
        }
        response = self.client.post("/api/register/", data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("user with this email already exists", str(response.data))
        self.assertIn("user with this username already exists", str(response.data))

    def test_login_and_token_generation(self):
        user = User.objects.create_user(
            username="author",
            email="auth_login@example.com",
            password="TestPass123",
            role="author",
            phone="1234567890",
            pincode="123456"
        )
        response = self.client.post("/api/login/", {
            "username": "author",
            "password": "TestPass123"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.data)


class ContentPermissionTests(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='Admin123',
            role='admin',
            phone='9999999999',
            pincode='123456'
        )
        self.author1 = User.objects.create_user(
            username='author1',
            email='author1@example.com',
            password='Author123',
            role='author',
            phone='1234567890',
            pincode='123456'
        )
        self.author2 = User.objects.create_user(
            username='author2',
            email='author2@example.com',
            password='Author123',
            role='author',
            phone='1234567891',
            pincode='123457'
        )

        self.admin_token = Token.objects.create(user=self.admin)
        self.author1_token = Token.objects.create(user=self.author1)
        self.author2_token = Token.objects.create(user=self.author2)

        self.content = Content.objects.create(
            title="Sample",
            body="This is a sample content",
            summary="Sample summary",
            categories="tech",
            author=self.author1
        )

    def test_author_can_create_content(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.author1_token.key)
        data = {
            "title": "New Title",
            "body": "New body content",
            "summary": "Short summary",
            "categories": "dev"
        }
        response = self.client.post("/api/content/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_duplicate_title_for_same_author(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.author1_token.key)
        data = {
            "title": "Sample",  # already created in setUp
            "body": "Another body",
            "summary": "New Summary",
            "categories": "tech"
        }
        response = self.client.post("/api/content/", data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("already created content with this title", str(response.data))

    def test_author_can_edit_own_content(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.author1_token.key)
        response = self.client.put(f"/api/content/{self.content.id}/", {
            "title": "Updated Title",
            "body": "Updated body",
            "summary": "Updated summary",
            "categories": "tech"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_author_cannot_edit_others_content(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.author2_token.key)
        response = self.client.put(f"/api/content/{self.content.id}/", {
            "title": "Hack Title",
            "body": "Hack body",
            "summary": "Hacked",
            "categories": "hacked"
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_edit_any_content(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.put(f"/api/content/{self.content.id}/", {
            "title": "Admin Updated",
            "body": "Admin body",
            "summary": "Admin summary",
            "categories": "admin"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
