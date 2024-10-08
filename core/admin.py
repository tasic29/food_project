from django.contrib import admin
from .models import MyUser
# Register your models here.


@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name']
    search_fields = ['username__icontains',
                     'first_name__icontains', 'last_name__icontains']
