import uuid
import requests
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.urls import reverse
from django.conf import settings
from apps.account.form import LoginForm
from apps.account.models import GithubUser, Users
from utils.time_utils import iso8601_to_datetime


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


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
    access_token = req.text.split("&")[0].split("=")[1]
    if access_token == "incorrect_client_credentials":
        return HttpResponse("<h1>获取token错误</h1>")
    else:
        user_url = "https://api.github.com/user"
        headers = {
            "Authorization": "token " + access_token
        }
        user_auth_result = requests.get(user_url, headers=headers).json()
        dbUser = auth_to_db(user_auth_result)
        user = authenticate(username=dbUser.username, password=settings.SECRET_KEY)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        return HttpResponse("<h1>Login Failed</h1>")


def auth_to_db(user_info_dict):
    user_info_dict["gid"] = user_info_dict.pop("id")
    user_info_dict['created_at'] = iso8601_to_datetime(user_info_dict['created_at'])
    user_info_dict['updated_at'] = iso8601_to_datetime(user_info_dict['updated_at'])
    remove_field = ["node_id", "gravatar_id", "twitter_username", "hireable"]
    for k in remove_field:
        user_info_dict.pop(k, None)
    gid = user_info_dict['gid']
    gitusers = GithubUser.objects.filter(gid=gid)
    if gitusers.exists():
        gituser = gitusers[0]
    else:
        # 不存在则创建
        gituser = GithubUser.objects.create(**user_info_dict)
    # 用户常用更新信息
    gituser.name = user_info_dict.get("name", "")
    gituser.email = user_info_dict.get("email", "")
    gituser.bio = user_info_dict.get("bio", "")
    gituser.location = user_info_dict.get("location", "")
    gituser.avatar_url = user_info_dict.get("avatar_url", "")
    gituser.followers = user_info_dict.get("followers", 0)
    gituser.following = user_info_dict.get("following", 0)
    gituser.public_repos = user_info_dict.get("public_repos", 0)
    gituser.updated_at = user_info_dict.get("updated_at", "")
    gituser.save()

    # 新建或更新至当前系统用户表
    if gituser.user is None:
        user = Users()
        user.username = gituser.login
        user.email = gituser.email if gituser.email else f"{gituser.login}@github.com"
        user.set_password(settings.SECRET_KEY)
        user.avatar = gituser.avatar_url
        user.nickname = gituser.name
        user.save()
        # 关联github用户和当前系统用户
        gituser.user = user
        gituser.save()
    else:
        gituser.user.avatar = gituser.avatar_url
        gituser.user.nickname = gituser.name
        gituser.user.save()

    return gituser.user