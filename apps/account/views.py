import uuid
import requests
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.urls import reverse
from django.conf import settings
from apps.account.form import LoginForm


# Create your views here.
def login_view(request):
    context = {}
    if request.method == "GET":
        context['form'] = LoginForm
        return render(request, "login.html", context)
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
    return HttpResponse("<h1>Login Failed</h1>")


def auth_github_view(request):
    url = f"https://github.com/login/oauth/authorize?scope=user:email&" \
          f"client_id={settings.AUTH['github']['client_id']}&state={uuid.uuid4().hex}"
    return HttpResponseRedirect(url)


def auth_github_callback(request):
    code = request.GET.get("code", None)
    state = request.GET.get("state", None)
    if code is None or state is None:
        return HttpResponseBadRequest(reason="参数错误")

    token_url = "https://github.com/login/oauth/access_token"

    data = {
        "client_id": settings.AUTH['github']['client_id'],
        "client_secret": settings.AUTH['github']['client_secret'],
        "code": code,
        "state": state
    }
    req = requests.post(token_url, data=data)
    result = req.text.split("&")
    access_token = result[0].split("=")[1]
    if access_token == "bad_verification_code":
        return HttpResponseBadRequest(reason="获取token错误")
    user_url = "https://api.github.com/user?access_token=" + access_token
    headers = {
        "Authorization": "token " + access_token
    }
    user_auth_result = requests.get(user_url, headers=headers).json()
    print(user_auth_result)
