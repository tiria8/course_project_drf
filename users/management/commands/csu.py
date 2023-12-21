from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            user_email='titadarenka@gmail.com',
            first_name='Daria',
            last_name='Titarenko',
            is_staff=True,
            is_superuser=True,
        )

        user.set_password('dasha888')
        user.save()
