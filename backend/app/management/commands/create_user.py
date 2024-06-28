from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from app.models import Officer


class Command(BaseCommand):
    help = 'Create a new user and associated officer'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument('name', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('identifier', type=str)

    def handle(self, *args, **kwargs):
        name = kwargs['name']
        username = kwargs['username']
        email = kwargs['email']
        password = kwargs['password']
        identifier = kwargs['identifier']

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR(f'User {username} already exists'))
            return

        user = User.objects.create_user(username=username, email=email, password=password)
        officer = Officer.objects.create(user=user, name=name, identifier=identifier)

        self.stdout.write(self.style.SUCCESS(f'Successfully created user and officer with username {username}'))
