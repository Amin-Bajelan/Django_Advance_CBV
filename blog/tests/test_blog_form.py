from django.test import SimpleTestCase, TestCase
from ..forms import PostForm
from datetime import datetime

from ..models import Category


class TestForms(TestCase):
    def test_post_with_valid_data(self):
        category_obj = Category.objects.create(name='Test Category')
        my_form = PostForm(data={
            'title': 'Test Post',
            'content': 'Test Content',
            'status': 'True',
            'category': category_obj,
            'published_date': datetime.now(),
        })
        self.assertTrue(my_form.is_valid())

    def test_post_with_no_data(self):
        my_form = PostForm(data={})
        self.assertFalse(my_form.is_valid())
