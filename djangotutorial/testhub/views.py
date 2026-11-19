from datetime import timezone

from django.db.models import Count, Sum
from django.shortcuts import render, redirect, get_object_or_404

from .forms import TestStartForm
from .models import Test

# Ключ сесії, де зберігаються id результатів, які цей відвідувач може переглядати
RESULTS_SESSION_KEY = "testhub_results"


def _attempt_key(test_id):
    """Ключ сесії з даними поточної спроби (ПІБ + час початку)."""
    return f"testhub_attempt_{test_id}"

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

def test_start(request, test_id):
    # Крок 1: вводимо ПІБ, після чого запускається таймер
    test = get_object_or_404(Test, pk=test_id, is_active=True)

    if request.method == "POST":
        form = TestStartForm(request.POST)
        if form.is_valid():
            request.session[_attempt_key(test.id)] = {
                **form.cleaned_data,
                "started_at": timezone.now().isoformat(),
            }
            return redirect("testhub:take", test_id=test.id)
    else:
        form = TestStartForm()

    return render(request, "testhub/test_start.html", {
        "test": test,
        "form": form,
        "questions_count": test.questions.count(),
    })

def test_pass(request, test_id):
    test = get_object_or_404(Test, id=test_id)

    # Перевіряємо, чи ввів користувач дані на попередній сторінці
    user_data = request.session.get(f'test_{test_id}_user')
    if not user_data:
        return redirect('start', test_id=test.id)

    questions = test.questions.all()  # Або Question.objects.filter(test=test)

    if request.method == 'POST':
        score = 0
        total = questions.count()

        for question in questions:
            # Отримуємо ID обраної відповіді для кожного питання
            selected_choice_id = request.POST.get(f'question_{question.id}')
            if selected_choice_id:
                choice = Choice.objects.filter(
                    id=selected_choice_id, question=question
                ).first()
                if choice and choice.is_correct:
                    score += 1

        # Зберігаємо результат у сесію (або в БД)
        request.session[f'test_{test_id}_result'] = {
            'score': score,
            'total': total,
        }
        return redirect('test_result', test_id=test.id)

    context = {
        'test': test,
        'questions': questions,
        'user_data': user_data,
    }
    return render(request, 'tests/test_pass.html', context)


def test_result(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    user_data = request.session.get(f'test_{test_id}_user')
    result_data = request.session.get(f'test_{test_id}_result')

    if not user_data or not result_data:
        return redirect('start', test_id=test.id)

    context = {
        'test': test,
        'user_data': user_data,
        'result': result_data,
    }
    return render(request, 'tests/test_result.html', context)