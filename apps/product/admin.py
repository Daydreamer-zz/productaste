from django.contrib import admin
from apps.product.models import Product


class ProductAdmin(admin.ModelAdmin):
    fieldsets = (
        # 产品主要信息区域
        ["Main",
            {
                "fields": ("name", "url", "digest")
            }
        ],
        # 产品高级信息区域
        ["Advance",
            {
                "fields": ("user", "public", "remark"),
                # 点击才显示高级区域
                "classes": ("collapse", )
            }
        ]
    )
    # 列表显示字段
    list_display = ("pid", "name", "digest", "user", "public")


admin.site.register(Product, ProductAdmin)