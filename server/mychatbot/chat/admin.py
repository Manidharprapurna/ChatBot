from django.contrib import admin
from .models import Department, FAQ

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('id', 'department', 'question', 'is_active', 'created_at')
    list_filter = ('department', 'is_active')
    search_fields = ('question', 'answer')
    list_editable = ('is_active',)