from .models import Category
from django.db.models import Avg, Count, Sum


def active_categories(request):
    categories = Category.objects.annotate(category_items=Count('item')).order_by('-category_items')\
        .filter(category_items__gt=0)
    return dict(categories=categories)