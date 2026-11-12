from django.db.models import Count, Sum
from django.shortcuts import render
from .models import Test

def test_list(request):
    # Отримуємо всі тести з БД
    tests = (
        Test.objects
        .annotate(
            questions_count = Count('questions'),
            total_points = Sum('questions__points'),
        )
        .order_by('-created_at')
    )
    # Передаємо їх у шаблон через словник context
    return render(request, 'testhub/test_list.html', {'tests': tests})
