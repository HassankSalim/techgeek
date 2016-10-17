from django.contrib import admin

# Register your models here.
from .models import Questions,User,Options

admin.site.register(Questions)
admin.site.register(User)
admin.site.register(Options)
