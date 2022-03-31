from django.contrib import admin
from django.utils.safestring import mark_safe
from apps.account.models import Users, GithubUser
from apps.product.models import Product


class ProductInline(admin.TabularInline):
    model = Product


class UsersAdmin(admin.ModelAdmin):
    def avatar_view(self, obj):
        html_tag = f"""<div><img style="width: 50px" src="{obj.avatar}"></div>"""
        return mark_safe(html_tag)
    avatar_view.short_description = "头像"
    list_display = ("uid", "username", "nickname", "avatar_view", "is_active", "is_staff", )
    # 用户详细页面显示相关联产品信息(内联进来)
    inlines = [ProductInline]


admin.site.register(Users, UsersAdmin)
admin.site.register(GithubUser)
