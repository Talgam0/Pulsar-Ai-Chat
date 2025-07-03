# chat/urls.py
from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('session/<int:session_id>/', views.chat_session, name='chat_session'),
    path('new/', views.new_chat, name='new_chat'),
    path('send-message/', views.send_message, name='send_message'),
    path('history/', views.chat_history, name='history'),
]
