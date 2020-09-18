from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from .models import Question, Answer, User, Subject,Profile

admin.site.register(Question)
admin.site.register(Answer)
# admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Subject)
# admin.site.register(User, UserAdmin)