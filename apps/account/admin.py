from django.contrib import admin
from apps.account.models import Users, GithubUser
from apps.product.models import Product


class ProductInline(admin.TabularInline):
    model = Product


class UsersAdmin(admin.ModelAdmin):
    list_display = ("uid", "username", "nickname", "is_active", "is_staff", )
    # 用户详细页面显示相关联产品信息(内联进来)
    inlines = [ProductInline]


admin.site.register(Users, UsersAdmin)
admin.site.register(GithubUser)
