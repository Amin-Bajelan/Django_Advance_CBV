from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from accounts.models import User, Profile
from blog.models import Post, Category
from datetime import datetime
import random

category_list = ['It', 'Design', 'Developer', "Programmer"]


class Command(BaseCommand):
    help = "inserting dummy data"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.faker = Faker()

    def handle(self, *args, **options):
        user = User.objects.create_user(email=self.faker.email(), password='amin@123')
        profile = Profile.objects.get(username=user)
        profile.first_name = self.faker.first_name()
        profile.last_name = self.faker.last_name()
        profile.description = self.faker.paragraph(nb_sentences=1)
        print(profile.description)
        profile.save()

        for item in category_list:
            Category.objects.get_or_create(name=item)

        for i in range(10):
            Post.objects.create(author=profile,
                                title=self.faker.paragraph(nb_sentences=1),
                                content=self.faker.paragraph(nb_sentences=3),
                                status=random.choice([True, False]),
                                category=Category.objects.get(name=random.choice(category_list)),
                                published_date=datetime.now()
                                )
