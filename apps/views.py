#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from django.shortcuts import render
from apps.product.models import Product
from utils.time_utils import form_date


def index_view(request):
    products = {}
    for i in range(3):
        _date = form_date(i).date()
        res = Product.objects.filter(public=True, create_at__contains=_date).order_by("-create_at", "-vote_count")
        products[_date.strftime("%Y-%m-%d")] = res
    return render(request, "index.html", {"products_dict": products})
