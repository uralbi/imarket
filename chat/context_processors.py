from itertools import chain
from accounts.models import Account
from .models import Chat
from django.db.models import Q


def my_messages(request):
    if request.user.is_authenticated:
        msgs = Chat.objects.filter(Q(sender=request.user) | Q(receiver=request.user)).order_by('-created_at')
    else:
        msgs = None
    return dict(msgs=msgs)


def msgs_users(request):
    if request.user.is_authenticated:
        snd_ers = Chat.objects.filter(
            Q(sender=request.user)).values('receiver').distinct().values_list('receiver', flat=True)
        rcv_ers = Chat.objects.filter(
            Q(receiver=request.user)).values('sender').distinct().values_list('sender', flat=True)
        u_list = [i for i in chain(snd_ers, rcv_ers)]
        msg_users = Account.objects.filter(id__in=u_list).order_by('first_name')
    else:
        msg_users = None
    return dict(msg_users=msg_users)

