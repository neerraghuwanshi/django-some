from django.contrib import admin
from .models import blog, Comment

# Register your models here.

admin.site.register(blog)
admin.site.register(Comment)