from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect


urlpatterns = [
    path('', lambda request: redirect('/accounts/login/')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('projects/', include('projects.urls')),
    path('tasks/', include('tasks.urls')),
    path('teams/', include('teams.urls')),
    path('reports/', include('reports.urls')),
    path('files/', include('files.urls')),
    path('notifications/', include('notifications.urls')),
    path('chat/', include('chat.urls')),
]