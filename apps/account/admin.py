from django.contrib import admin
from apps.account.models import Users, GithubUser

# Register your models here.
admin.site.register(Users)
admin.site.register(GithubUser)
