from django.urls import path
from notifications import views

urlpatterns = [
    path('', views.notification_list, name='notification_list'),
    path('<int:pk>/read/', views.notification_read, name='notification_read'),
    path('read-all/', views.notification_read_all, name='notification_read_all'),
    path('<int:pk>/delete/', views.notification_delete, name='notification_delete'),
    path('delete-all/', views.notification_delete_all, name='notification_delete_all'),
]