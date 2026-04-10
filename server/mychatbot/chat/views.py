from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
import json

from .chatbot import get_response
from .models import Department, FAQ


def home(request):
    return render(request, 'chat/home.html')


@csrf_exempt
@require_POST
def get_bot_response(request):
    try:
        data = json.loads(request.body)

        # support both keys (Postman + frontend)
        user_text = data.get('user_message', data.get('msg', ''))
        user_text = user_text.strip() if isinstance(user_text, str) else ''

    except (json.JSONDecodeError, AttributeError):
        user_text = ''

    if not user_text:
        return JsonResponse({
            'response': "I didn't receive a message. Could you try again?",
            'source': 'none'
        })

    # CALL CHATBOT (returns dict now)
    result = get_response(user_text)

    return JsonResponse({
        'response': result.get('response', ''),
        'source': result.get('source', 'unknown')  
    })


@require_GET
def get_departments(request):
    departments = list(
        Department.objects.values('id', 'name', 'description')
    )
    return JsonResponse({'departments': departments})


@require_GET
def get_department_questions(request, dept_id):
    faqs = list(
        FAQ.objects
        .filter(department_id=dept_id, is_active=True)
        .values('id', 'question')
        .order_by('created_at')
    )
    return JsonResponse({'questions': faqs})


@require_GET
def get_faq_answer(request, faq_id):
    try:
        faq = FAQ.objects.get(id=faq_id, is_active=True)
        return JsonResponse({'answer': faq.answer})
    except FAQ.DoesNotExist:
        return JsonResponse({'error': 'FAQ not found'}, status=404)