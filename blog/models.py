from django.db import models
from accounts.models import User, Profile
from django.urls import reverse

#Create your models here.

class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="post/", null=True, blank=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    status = models.BooleanField()
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateField()

    def __str__(self):
        return self.title

    def get_snip(self):
        return self.content[0:5]

    def get_absolute_api_url(self):
        return reverse('blog:api-v1:post-detail', kwargs={'pk': self.pk})


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
