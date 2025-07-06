from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from django.views.generic import detail

from ..views import RedirectToGoogle, DetailPost, ListPost


# Create your tests here.

class TestUrl(SimpleTestCase):

    def test_blog_index_url_resolve(self):
        url = reverse('blog:redirect')
        self.assertEqual(resolve(url).func.view_class, RedirectToGoogle)

    def test_post_detail(self):
        url = reverse('blog:post_detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, DetailPost)

    def test_post_list(self):
        url = reverse('blog:about')
        self.assertEqual(resolve(url).func.view_class, ListPost)
