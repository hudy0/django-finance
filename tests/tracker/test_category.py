from django.test import TestCase

from tracker.models import Category


class CategoryModelTestCase(TestCase):
    def test_create_category(self):
        category = Category.objects.create(name="Test Category")
        self.assertEqual(str(category), "Test Category")

    def test_str_representation(self):
        category = Category(name="Test Category")
        self.assertEqual(str(category), "Test Category")

    def test_verbose_name_plural(self):
        self.assertEqual(str(Category._meta.verbose_name_plural), "Categories")
