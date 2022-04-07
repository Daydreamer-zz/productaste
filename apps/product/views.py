from django.shortcuts import render
from apps.product.models import Product
from apps.product.form import ProductForm
from django.http import HttpResponseRedirect, HttpResponse,HttpResponseForbidden
from django.urls import reverse


# Create your views here.
def add_new_product(request):
    if request.user.is_authenticated:
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            user = request.user
            product.user = user
            product.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponse("<h1>表单内容错误</h1>")
    else:
        return HttpResponseForbidden("<h1>请先登录</h1>")
