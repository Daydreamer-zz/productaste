from django.contrib import admin
from apps.account.models import Users, GithubUser


class UsersAdmin(admin.ModelAdmin):
    list_display = ("uid", "username", "nickname", "is_active", "is_staff", )


admin.site.register(Users, UsersAdmin)
admin.site.register(GithubUser)
