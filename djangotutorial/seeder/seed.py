from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Наповнює базу даних фейковими користувачами'

    def add_arguments(self, parser):
        # Дозволяє вказувати кількість користувачів через аргумент (дефолт: 10)
        parser.add_argument(
            '--total',
            type=int,
            default=10,
            help='Кількість користувачів для створення'
        )

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        fake = Faker(['uk_UA', 'en_US'])  # Підтримка українських та англійських імен

        self.stdout.write(f'Початок створення {total} користувачів...')

        created_count = 0
        for _ in range(total):
            profile = fake.simple_profile()
            username = profile['username']
            email = profile['mail']

            # Перевіряємо, чи користувач вже існує
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(
                    username=username,
                    email=email,
                    password='Password123!',  # Стандартний пароль для всіх тест-аккаунтів
                    first_name=fake.first_name(),
                    last_name=fake.last_name()
                )
                created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Успішно створено {created_count} нових користувачів із {total} запрошених.'
        ))
