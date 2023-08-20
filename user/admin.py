from django.contrib import admin

from .models import User 

#regustering the User model in the admin site.
admin.site.register(User)
