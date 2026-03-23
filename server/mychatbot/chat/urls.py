from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('get/', views.get_bot_response, name='get_bot_response'),
    path('api/departments/', views.get_departments, name='get_departments'),
    path('api/departments/<int:dept_id>/questions/', views.get_department_questions, name='get_department_questions'),
    path('api/faq/<int:faq_id>/answer/', views.get_faq_answer, name='get_faq_answer'),
]