from django.urls import path

from testhub import views

app_name = 'testhub'

urlpatterns = [
    path('', views.test_list, name='list'),
    path('<int:test_id>/', views.test_start, name='start'),
    path('<int:test_id>/pass/', views.test_pass, name='test_pass'),
    path('<int:test_id>/result/', views.test_result, name='test_result'),
]
