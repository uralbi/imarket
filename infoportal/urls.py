import os
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
from django.conf.urls.static import static
from django.conf import settings
from django.urls import re_path
from .settings import BASE_DIR
from .views import HomePage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePage.as_view(), name='home'),
    path('accounts/', include('accounts.urls')),
    path('items/', include('market.urls')),
    path('msgs/', include('chat.urls')),
    re_path(r'^icons/(?P<path>.*)$', serve,
        {'document_root': os.path.join(BASE_DIR, 'media/icons'),
         'show_indexes': True}, name='icons')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

