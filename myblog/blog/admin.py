from django.contrib import admin

from .models import Comment, Entry

# Register your models here.

admin.site.register(Entry)
admin.site.register(Comment)