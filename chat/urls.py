from django.urls import path
from chat import views

urlpatterns = [
    path('', views.chat_list, name='chat_list'),
    path('<int:room_id>/', views.chat_room, name='chat_room'),
]