from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('send_msg/', chat_msg, name='send_msg'),
    path('delete_msg/', delete_msg, name='delete_msg'),
    path('my_messages/', login_required(MyMsgs.as_view()), name='my_msgs')
]