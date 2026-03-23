from django.shortcuts import render
from django.http import JsonResponse
from .chatbot import get_response
from .models import Department, FAQ

def home(request):
    return render(request, 'chat/home.html')

def get_bot_response(request):
    user_text = request.GET.get('msg')
    if not user_text:
        return JsonResponse({'response': "I didn't receive a message. Could you try again?"})
    response = get_response(user_text)
    return JsonResponse({'response': response})

# --- New endpoints for Rule-Based FAQ Bot ---

def get_departments(request):
    departments = list(Department.objects.values('id', 'name', 'description'))
    return JsonResponse({'departments': departments})

def get_department_questions(request, dept_id):
    faqs = list(FAQ.objects.filter(department_id=dept_id).values('id', 'question'))
    return JsonResponse({'questions': faqs})

def get_faq_answer(request, faq_id):
    try:
        faq = FAQ.objects.get(id=faq_id)
        return JsonResponse({'answer': faq.answer})
    except FAQ.DoesNotExist:
        return JsonResponse({'error': 'FAQ not found'}, status=404)