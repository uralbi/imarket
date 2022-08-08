from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import DetailView, CreateView, ListView, DeleteView, UpdateView
from django.shortcuts import redirect
from django.urls import reverse_lazy, resolve
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
from django.template.defaultfilters import slugify
from django.db.models import Q
from accounts.models import Account
from category.models import Category
from .models import Item, ItemGallery, SavedItem
from .forms import Item_Creation_Form, GalleryForm, SavedItem_Form


class Item_Detail_View(DetailView):
    model = Item
    template_name = 'market/item_detail_view.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # saved all existed data
        context['gallery'] = ItemGallery.objects.filter(item=self.kwargs['pk'])
        if self.request.user.is_authenticated:
            s_items = SavedItem.objects.filter(user = self.request.user).filter(user=self.request.user, item_id = self.kwargs['pk']).exists()
            if s_items:
                context['saved'] = True
        else:
            context['saved'] = False
        return context


class ItemCreate(CreateView):
    model = Item
    form_class = Item_Creation_Form
    template_name = 'market/item_create.html'
    #default template_name:  Item_create_form // _create_form

    def get_context_data(self, *, objects_list=None, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page'] = 'Post'
        ctx['url_name'] = 'add_item'
        return ctx

    def get_success_url(self):
        user = self.request.user
        return reverse_lazy('my_items', kwargs={"pk": user.id})

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(self.request.POST['item_name'])
        return super().form_valid(form)


class MyItems(ListView):
    model = Item
    template_name = 'market/my_items.html'
        # default object name: object_list
        # adding new object name:
    context_object_name = 'items'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # saved all existed data
        context['gallery'] = ItemGallery.objects.filter(item__author_id=self.request.user.id)
        context['total_items'] = Item.objects.filter(author_id=self.request.user.id).count()
        return context

    def get_queryset(self):
        objects = Item.objects.filter(author_id=self.request.user.id).order_by('-modified_date')
        return objects


class ViewByCategory(ListView):
    model = Item
    template_name = 'market/by_category.html'
    context_object_name = 'items'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # saved all existed data
        context['gallery'] = ItemGallery.objects.filter(item__category=self.kwargs['category_id'])
        context['current_category'] = Category.objects.get(id = self.kwargs['category_id'])
        return context

    def get_queryset(self):
        objects = Item.objects.filter(category=self.kwargs['category_id']).order_by('-modified_date')
        return objects


class ItemDeleteView(UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model=Item
    context_object_name = 'item'
    success_message = 'Item has been deleted!'

    def get_success_url(self):
        user = self.request.user
        return reverse_lazy('my_items', kwargs={"pk": user.id})

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object().author_id
        if self.request.user.id == post:
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
                handler = getattr(self, 'delete')
            else:
                handler = self.http_method_not_allowed
        else:
            handler = self.http_method_not_allowed
            return redirect('home')
        return handler(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(ItemDeleteView, self).delete(request, *args, **kwargs)


class AddGalleryView(CreateView):
    model = ItemGallery
    form_class = GalleryForm
    template_name = 'market/my_items.html'
    #default template_name:  Item_create_form // _create_form

    def get_context_data(self, *, objects_list=None, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['gallery'] = ItemGallery.objects.filter(item__author_id=self.request.user.id)
        ctx['items'] = Item.objects.filter(author_id = self.request.user.id).order_by('-modified_date')
        return ctx

    def get_success_url(self):
        user = self.request.user
        return reverse_lazy('my_items', kwargs={"pk": user.id})

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.item_id = self.kwargs['item_id']
        return super().form_valid(form)


class Item_Update_View(SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    model = Item
    form_class = Item_Creation_Form
    template_name = 'market/item_create.html'
    success_message = 'Item has been updated!'

    def get_context_data(self, *, objects_list=None, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page'] = 'Update'
        ctx['update'] = True
        return ctx

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def get_success_url(self):
        user = self.request.user
        return reverse_lazy('my_items', kwargs={"pk": user.id})


class Image_Delete_Gallery(DeleteView):
    model=ItemGallery
    context_object_name = 'image'
    success_message = 'Image has been deleted from the Gallery!'

    def get_success_url(self):
        user = self.request.user
        return reverse_lazy('my_items', kwargs={"pk": user.id})

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object().item.id
        author_id = Item.objects.get(id = post).author_id
        if self.request.user.id == author_id:
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
                handler = getattr(self,'delete')
            else:
                handler = self.http_method_not_allowed
        else:
            handler = self.http_method_not_allowed
            return redirect('home')
        return handler(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(Image_Delete_Gallery, self).delete(request, *args, **kwargs)


class Next_ItemView(ListView):
    model = Item
    template_name = 'market/item_detail_view.html'
    context_object_name ='item'

    def get_context_data(self, *, objects_list=None, **kwargs):
        ctx = super().get_context_data(**kwargs)

        obj = Item.objects.all().select_related('category')
        curr_item = obj.get(id = self.kwargs['item_id'])
        curr_cat = curr_item.category
        if obj.filter(category=curr_item.category, pk__gt = curr_item.pk).exists():
            item = obj.filter(category=curr_item.category, pk__gt = curr_item.pk).order_by('id').first()
        else:
            ctx['no_next'] = True
            item = curr_item
        ctx['gallery'] = ItemGallery.objects.filter(item=item)

        if self.request.user.is_authenticated:
            s_items = SavedItem.objects.filter(user=self.request.user).filter(user=self.request.user,
                                                                          item_id=item.id).exists()
            if s_items:
                ctx['saved'] = True
        else:
            ctx['saved'] = False
        return ctx

    def get_queryset(self):
        obj = Item.objects.all().select_related('category')
        curr_item = obj.get(id = self.kwargs['item_id'])
        curr_cat = curr_item.category
        if obj.filter(category=curr_item.category, pk__gt = curr_item.pk).exists():
            item = obj.filter(category=curr_item.category, pk__gt = curr_item.pk).order_by('id').first()
        else:
            item = curr_item
        return item


class Prev_ItemView(ListView):
    model = Item
    template_name = 'market/item_detail_view.html'
    context_object_name ='item'

    def get_context_data(self, *, objects_list=None, **kwargs):
        ctx = super().get_context_data(**kwargs)
        obj = Item.objects.all().select_related('category')
        curr_item = obj.get(id = self.kwargs['item_id'])
        curr_cat = curr_item.category
        if obj.filter(category=curr_item.category, pk__lt = curr_item.pk).exists():
            item = obj.filter(category=curr_item.category, pk__lt = curr_item.pk).order_by('id').last()
        else:
            item = curr_item
            ctx['no_prev'] = True
        ctx['gallery'] = ItemGallery.objects.filter(item=item)

        if self.request.user.is_authenticated:
            s_items = SavedItem.objects.filter(user=self.request.user).filter(user=self.request.user,
                                                                          item_id=item.id).exists()
            if s_items:
                ctx['saved'] = True
        else:
            ctx['saved'] = False
        return ctx

    def get_queryset(self):
        obj = Item.objects.all().select_related('category')
        curr_item = obj.get(id=self.kwargs['item_id'])
        curr_cat = curr_item.category
        if obj.filter(category=curr_item.category, pk__lt=curr_item.pk).exists():
            item = obj.filter(category=curr_item.category, pk__lt=curr_item.pk).order_by('id').last()
        else:
            item = curr_item
        return item


class Item_Search_View(ListView):
    model = Item
    context_object_name = 'items'
    template_name = 'market/search_results.html'
    paginate_by = 40

    def get_context_data(self, *, objects_list=None, **kwargs):

        ctx = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        if len(query) < 3:
            ctx['min_char'] = 'Minimun 3 characters are required'
        else:
            ctx['min_char'] = ''
        return ctx

    def get_queryset(self):
        query = self.request.GET.get('q')
        query_list = query.split(" ")
        if len(query) < 3:
            return False
        obj = Item.objects.all()
        for i, q in enumerate(query_list):
            obj = obj.filter(Q(item_name__icontains=q) | Q(description__icontains=q)).order_by(
                '-modified_date')
        return obj


class Item_Search2_View(ListView):
    model = Item
    context_object_name = 'items'
    template_name = 'market/search_results.html'
    paginate_by = 40

    def get_queryset(self):
        q = self.request.GET.get('q')
        q_list = q.split(" ")
        q2 = self.request.GET.get('q2')
        q2_list = q2.split(" ")
        obj = Item.objects.all()
        for q in q_list:
            obj = obj.filter(Q(item_name__icontains=q) | Q(description__icontains=q)).order_by(
                '-modified_date')
        for q2 in q2_list:
            obj = obj.filter(Q(item_name__icontains=q2) | Q(description__icontains=q2)).order_by(
                '-modified_date')
        return obj


@login_required(login_url='home')
def create_save_item(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        user = Account.objects.get(email = request.POST['user'])
        item = Item.objects.get(id = request.POST['item'])
        form = SavedItem_Form({'user': user, 'item': item})
        if form.is_valid():
            s_item = SavedItem.objects.create(item=item, user=user)
            s_item.save()
            messages.success(request, 'Item is saved!')
        elif 'already exists' in f'{form.errors}':
            messages.error(request, 'Item is already in your saved list')
    return redirect(url)


@login_required()
def delete_save_item(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        user = Account.objects.get(email = request.user)
        item = Item.objects.get(id=request.POST['item2'])
        s_item = SavedItem.objects.filter(item_id = item, user = user)
        if s_item.exists():
            s_item.delete()
            messages.success(request, 'Item is removed from your saved list!')
    return redirect(url)


class SavedItems_View(LoginRequiredMixin, ListView):
    model = SavedItem
    template_name = 'market/saved_items.html'
    context_object_name = 'items'

    def get_queryset(self):
        obj = None
        return obj