#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from datetime import timedelta
from django.shortcuts import render
from apps.product.models import Product
from apps.product.form import ProductForm
from utils.time_utils import form_date, str2date


def index_view(request):
    last_dt = request.GET.get("last_dt", None)
    if last_dt is None:
        products = {}
        for i in range(3):
            _date = form_date(i).date()
            res = Product.objects.filter(public=True, created_at__contains=_date).order_by("-created_at", "-vote_count")
            products[_date.strftime("%Y-%m-%d")] = res
        context = {
            "products_dict": products,
            "form": ProductForm
        }
        return render(request, "index.html", context)
    else:
        _date = str2date(last_dt) + timedelta(-1)
        products = Product.objects.filter(public=True, created_at__contains=_date).order_by("-created_at", "-vote_count")
        context = {
            "date": _date.strftime("%Y-%m-%d"),
            "products": products
        }
        return render(request, "components/product_item.tpl.html", context)
