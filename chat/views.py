from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import ChatSession, Message
##import openai
from django.conf import settings

# Простая функция для генерации ответов (замените на реальный AI API)
def generate_ai_response(user_message):
    """
    Простая функция для генерации ответов.
    Замените на реальный AI API (OpenAI, Claude, etc.)
    """
    # Базовые ответы для демонстрации
    responses = {
        "привет": "Привет! Как дела? Я здесь, чтобы помочь вам.",
        "как дела": "У меня все хорошо, спасибо! Как у вас дела?",
        "помощь": "Я могу помочь вам с вопросами, связанными с аутизмом, поддержкой и общением.",
        "спасибо": "Пожалуйста! Рад помочь.",
    }
    
    user_message_lower = user_message.lower()
    
    # Поиск ключевых слов в сообщении
    for key, response in responses.items():
        if key in user_message_lower:
            return response
    
    # Ответ по умолчанию
    return f"Понимаю, что вы говорите: '{user_message}'. Это интересная тема. Можете рассказать больше?"

@login_required
def chat_view(request):
    """Главная страница чата"""
    # Получаем все сессии пользователя
    user_sessions = ChatSession.objects.filter(user=request.user).order_by('-updated_at')
    
    # Получаем или создаем активную сессию
    current_session = user_sessions.first()
    
    # Если у пользователя нет сессий, создаем новую
    if not current_session:
        current_session = ChatSession.objects.create(
            user=request.user,
            title='Новая беседа'
        )
        # Обновляем список сессий после создания новой
        user_sessions = ChatSession.objects.filter(user=request.user).order_by('-updated_at')
    
    # Получаем сообщения для текущей сессии
    messages = current_session.messages.all() if current_session else []
    
    context = {
        'current_session': current_session,
        'user_sessions': user_sessions,
        'messages': messages
    }
    
    return render(request, 'chat/chat.html', context)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def send_message(request):
    """Отправка сообщения в чат"""
    try:
        data = json.loads(request.body)
        message_content = data.get('message', '').strip()
        session_id = data.get('session_id')
        
        if not message_content:
            return JsonResponse({'error': 'Сообщение не может быть пустым'}, status=400)
        
        # Получаем или создаем сессию
        if session_id:
            session = get_object_or_404(ChatSession, id=session_id, user=request.user)
        else:
            session = ChatSession.objects.create(
                user=request.user,
                title=message_content[:50] + "..." if len(message_content) > 50 else message_content
            )
        
        # Сохраняем сообщение пользователя
        user_message = Message.objects.create(
            session=session,
            message_type='user',
            content=message_content
        )
        
        # Генерируем ответ ассистента
        ai_response = generate_ai_response(message_content)
        
        # Сохраняем ответ ассистента
        assistant_message = Message.objects.create(
            session=session,
            message_type='assistant',
            content=ai_response
        )
        
        # Обновляем время последнего обновления сессии
        session.save()
        
        return JsonResponse({
            'success': True,
            'user_message': {
                'id': user_message.id,
                'content': user_message.content,
                'created_at': user_message.created_at.strftime('%H:%M')
            },
            'assistant_message': {
                'id': assistant_message.id,
                'content': assistant_message.content,
                'created_at': assistant_message.created_at.strftime('%H:%M')
            },
            'session_id': session.id
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def new_chat(request):
    """Создание новой сессии чата"""
    session = ChatSession.objects.create(
        user=request.user,
        title='Новая беседа'
    )
    return redirect('chat:chat_session', session_id=session.id)

@login_required
def chat_session(request, session_id):
    """Просмотр конкретной сессии чата"""
    session = get_object_or_404(ChatSession, id=session_id, user=request.user)
    user_sessions = ChatSession.objects.filter(user=request.user).order_by('-updated_at')
    
    context = {
        'current_session': session,
        'user_sessions': user_sessions,
        'messages': session.messages.all()
    }
    
    return render(request, 'chat/chat.html', context)

@login_required
def chat_history(request):
    """История чатов пользователя"""
    sessions = ChatSession.objects.filter(user=request.user).order_by('-updated_at')
    return render(request, 'chat/history.html', {'sessions': sessions})
