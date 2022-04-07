#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from django import forms
from apps.product.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "url", "digest"]
