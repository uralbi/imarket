from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import DetailView, CreateView, ListView, DeleteView, UpdateView
from django.shortcuts import redirect
from django.db.models import Q, Count
from accounts.models import Account
from market.models import Item
from .forms import Chat_Form
from .models import Chat


@login_required()
def chat_msg(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        user = request.user
        receiver = Account.objects.get(email=request.POST['receiver'])
        item = Item.objects.get(id=request.POST['item'])
        msg = request.POST['msg']
        form = Chat_Form({'sender': user, 'receiver': receiver, 'subject': item, 'content': msg})
        if form.is_valid():
            s_msg = Chat.objects.create(sender=user, receiver=receiver, subject=item, content=msg)
            s_msg.save()
            messages.success(request, 'Message has been sent!')
        else:
            if 'Ensure this value has at most' in f'{form.errors}':
                messages.error(request, 'Maximum 100 characters are allowed!')
    return redirect(url)


@login_required()
def delete_msg(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        msg_id = request.POST['msg_id']
        msg_obj = Chat.objects.get(id=msg_id)
        if msg_obj:
            if request.user == msg_obj.sender:
                msg_obj.delete()
                messages.success(request, 'Message has been deleted!')
    return redirect(url)


class MyMsgs(ListView):
    model = Chat
    template_name = 'chat/chats.html'
    context_object_name = 'my_msgs'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # saved all existed data
        user = self.request.user
        objs = Chat.objects.filter(Q(sender=user) | Q(receiver=user)).values('subject').distinct()
        items = Item.objects.filter(id__in=objs)
        context['subs'] = items

        return context

    def get_queryset(self):
        user = self.request.user
        objs = Chat.objects.filter(Q(sender=user) | Q(receiver=user)).order_by('-created_at')
        return objs