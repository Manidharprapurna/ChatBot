from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .chatbot import get_response
from .models import Department, FAQ
import json


# Home Page
def home(request):
    return render(request, 'chat/home.html')


# CHATBOT (INTENTS.JSON)
@csrf_exempt
def get_bot_response(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            user_text = body.get("message")

            if not user_text:
                return JsonResponse({
                    'response': "I didn't receive a message. Please try again."
                })

            response = get_response(user_text)

            return JsonResponse({'response': response})

        except Exception as e:
            return JsonResponse({
                'response': "Something went wrong"
            })

    return JsonResponse({'response': 'Invalid request'})


# GET ALL DEPARTMENTS
def get_departments(request):
    departments = list(
        Department.objects.values('id', 'name', 'description')
    )
    return JsonResponse({'departments': departments})


#  GET QUESTIONS BY DEPARTMENT
def get_department_questions(request, dept_id):
    faqs = list(
        FAQ.objects.filter(department_id=dept_id)
        .values('id', 'question')
    )
    return JsonResponse({'questions': faqs})


# GET ANSWER BY FAQ ID
def get_faq_answer(request, faq_id):
    try:
        faq = FAQ.objects.get(id=faq_id)
        return JsonResponse({'answer': faq.answer})
    except FAQ.DoesNotExist:
        return JsonResponse({'error': 'FAQ not found'}, status=404)