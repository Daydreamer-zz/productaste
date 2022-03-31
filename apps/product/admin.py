from django.contrib import admin
from apps.product.models import Product, ProductVoteuser

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductVoteuser)