from django.test import TestCase
from accounts.models import User, Profile
from ..models import Post
from datetime import datetime


class BlogModelTest(TestCase):
    def test_create_post(self):
        user = User.objects.create_user(email='bajelan2@gmail.com', password='Amin@123')
        profile = Profile.objects.create(
            username=user,
            first_name='amin',
            last_name='bajelan',
            description='hahahaahaha',
        )
        my_post = Post.objects.create(
            author=profile,
            title='Test Post',
            content='Test Content',
            status='True',
            category=None,
            published_date=datetime.now(),
        )
        self.assertEqual(my_post.title, 'Test Post')

