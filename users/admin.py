from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'gender', 'phone', 'address', 'birth_date']
    list_filter = ['gender']
    list_select_related = ['user']
    search_fields = ['user__first_name', 'user__last_name', 'phone', 'address']