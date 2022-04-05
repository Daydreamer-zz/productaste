import uuid
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
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