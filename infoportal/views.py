from django.shortcuts import render
from market.models import Item, ItemGallery
from django.views.generic import ListView

# def home(request):
#     items = Item.objects.all().filter(is_active=True).order_by('-created_date')
#     pictures = ItemGallery.objects.all()
#
#     context = {
#         'items': items,
#         'pictures': pictures,
#     }
#
#     return render(request, 'index.html', context)


class HomePage(ListView):
    model = Item
    context_object_name = 'items'
    template_name = 'index.html'

    def get_queryset(self):
        objects = Item.objects.all().filter(is_active=True).order_by('-modified_date')[:100]
        return objects