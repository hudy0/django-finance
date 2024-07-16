from django.test import TestCase

from django_finance.accounts.models import User


class UserModelTestCase(TestCase):
    def test_user_inherits_from_abstract_user(self):
        """
        Test that the User model inherits from AbstractUser.
        """
        user = User()
        self.assertTrue(isinstance(user, User))

    def test_user_creation(self):
        """
        Test that a new User instance can be created.
        """
        user = User.objects.create_user(username="testuser", email="testuser@example.com", password="testpassword")
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "testuser@example.com")
        self.assertTrue(user.check_password("testpassword"))

    def test_user_superuser_creation(self):
        """
        Test that a new superuser can be created.
        """
        superuser = User.objects.create_superuser(
            username="superuser",
            email="superuser@example.com",
            password="superpassword",
        )
        self.assertEqual(superuser.username, "superuser")
        self.assertEqual(superuser.email, "superuser@example.com")
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.check_password("superpassword"))
