from django.test import TestCase
from .models import User
from django.test import TestCase
from rest_framework.exceptions import ValidationError
from .models import User
from .serializers import UserSerializer, TokenSerializer

class UserModelTest(TestCase):
    def test_email_unique(self):
        User.objects.create(email="unique@example.com", tg_id="11111111")
        with self.assertRaises(Exception):
            User.objects.create(email="unique@example.com", tg_id="22222222")

    def test_tg_id_unique(self):
        User.objects.create(email="user1@example.com", tg_id="99999999")
        with self.assertRaises(Exception):
            User.objects.create(email="user2@example.com", tg_id="99999999")



class UserSerializerTest(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }

    def test_password_write_only(self):
        """Проверка что password write_only"""
        user = User.objects.create(email='existing@example.com', password='testpass')
        serializer = UserSerializer(user)
        self.assertNotIn('password', serializer.data)

    def test_missing_email(self):
        """Проверка ошибки при отсутствии email"""
        invalid_data = {'password': 'testpass123'}
        serializer = UserSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_missing_password(self):
        """Проверка ошибки при отсутствии password"""
        invalid_data = {'email': 'test@example.com'}
        serializer = UserSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

class TokenSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='tokenuser@example.com',
            password='testpass123'
        )

    def test_get_token_contains_email(self):
        """Проверка, что email включен в токен"""
        token = TokenSerializer.get_token(self.user)
        self.assertIn('email', token.payload)
        self.assertEqual(token.payload['email'], 'tokenuser@example.com')

    def test_get_token_contains_username(self):
        """Проверка, что username включен в токен (несмотря на username=None в модели)"""
        token = TokenSerializer.get_token(self.user)
        self.assertIn('username', token.payload)
        self.assertIsNone(token.payload['username'])  # Так как у вас username=None в модели

    def test_token_serializer_with_valid_credentials(self):
        """Проверка получения токена с валидными учетными данными"""
        data = {
            'email': 'tokenuser@example.com',
            'password': 'testpass123'
        }
        serializer = TokenSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertIn('access', serializer.validated_data)
        self.assertIn('refresh', serializer.validated_data)

    def test_token_serializer_with_invalid_credentials(self):
        """Проверка ошибки при неверных учетных данных"""
        data = {
            'email': 'tokenuser@example.com',
            'password': 'wrongpassword'
        }
        serializer = TokenSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('detail', serializer.errors)