from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'due_date', 'status', 'responsible')
    list_filter = ('status', 'responsible')
    search_fields = ('title', 'description')
