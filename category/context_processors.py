from .models import Category
from django.db.models import Avg, Count, Sum


def active_categories(request):
    categories = Category.objects.all()
    return dict(categories=categories)