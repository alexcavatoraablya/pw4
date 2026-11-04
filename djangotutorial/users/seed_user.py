from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
import random

User = get_user_model()
fake = Faker(['uk_UA', 'en_US'])


class Command(BaseCommand):
    help = 'Генерує випадкових користувачів для бази даних'

    def add_arguments(self, parser):
        # Додаємо аргумент для вказання кількості користувачів (за замовчуванням 10)
        parser.add_argument(
            '--total',
            type=int,
            default=10,
            help='Кількість користувачів для створення'
        )

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        self.stdout.write(f'Початок генерації {total} користувачів...')

        created_count = 0
        for _ in range(total):
            username = fake.user_name()
            email = fake.unique.email()

            # Перевіряємо, чи немає користувача з таким username або email
            if not User.objects.filter(username=username).exists() and not User.objects.filter(email=email).exists():
                first_name = fake.first_name()
                last_name = fake.last_name()

                # Створюємо користувача з безпечним хешуванням пароля
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password='Password123!',  # Стандартний пароль для всіх тестових юзерів
                    first_name=first_name,
                    last_name=last_name
                )

                # Опціонально: робимо деяких користувачів персоналом/суперюзерами
                # if random.choice([True, False, False, False]):  # 25% шанс
                #     user.is_staff = True
                #     user.save()

                created_count += 1

        self.stdout.write(self.style.SUCCESS(f'Успішно створено {created_count} нових користувачів!'))
