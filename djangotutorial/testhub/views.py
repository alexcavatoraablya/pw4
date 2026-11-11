from django.shortcuts import render
from .models import Test

def test_list_view(request):
    # Отримуємо всі тести з БД
    tests = Test.objects.all()
    # Передаємо їх у шаблон через словник context
    return render(request, 'quiz/test_list.html', {'tests': tests})
