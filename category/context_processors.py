from .models import Category
from django.db.models import Avg, Count, Sum


def active_categories(request):
    categories = Category.objects.annotate(categoryitems=Count('item')).order_by('-categoryitems')\
        .filter(categoryitems__gt=0)
    return dict(categories=categories)