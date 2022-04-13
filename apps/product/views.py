import requests.utils
from django.shortcuts import render
from apps.product.models import Product
from apps.product.form import ProductForm
from apps.product.models import Product
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden, JsonResponse
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


def vote_product(request):
    p_id = request.POST.get("pid", None)
    if p_id is None:
        return JsonResponse({"errcode": 400, "message": "参数错误"})
    if request.user is None or not request.user.is_authenticated:
        return JsonResponse({"errcode": 401, "message": "用户未登录"})
    try:
        product = Product.objects.get(pid=p_id)
        product.vote(request.user)
        return JsonResponse({"errcode": 200, "message": "成功", "data": {
            "vote_count": product.vote_count
        }})
    except Product.DoesNotExist:
        return JsonResponse({"errcode": 404, "message": "产品不存在"})

