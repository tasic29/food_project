from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser
# Register your models here.


@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name']
    search_fields = ['username__icontains',
                     'first_name__icontains', 'last_name__icontains']
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2", 'first_name', 'last_name'),
            },
        ),
    )
