from django.shortcuts import render

from .models import Category

# Create your views here.

def category_list(request):
    categories = Category.objects.all().order_by("name")
    print(categories)
    return render(request, "categories/category_list.html", {"categories": categories})
