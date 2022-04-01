#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from django.shortcuts import render
from apps.product.models import Product


def index_view(request):
    products = Product.objects.filter(public=True).order_by("-create_at")
    context = {
        "products": products,
    }
    return render(request, "index.html", context)