from .models import Item, ItemGallery, SavedItem
from django.db.models import Avg, Count, Sum

def my_items_no(request):
    if request.user.is_authenticated:
        items_no = Item.objects.filter(author=request.user).count
    else:
        items_no = None
    return dict(items_no=items_no)

def saved_items(request):
    if request.user.is_authenticated:
        s_items = SavedItem.objects.filter(user=request.user).order_by('-created_at')
    else:
        s_items = None
    return dict(s_items=s_items)