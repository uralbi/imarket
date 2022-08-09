from .models import Category
from django.db.models import Avg, Count, Sum


def active_categories(request):
    objs = Category.objects.annotate(categoryitems=Count('item'))
    categories = objs.order_by('-categoryitems').filter(categoryitems__gt=0)
    return dict(categories=categories)