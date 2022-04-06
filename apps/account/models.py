from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from utils.id_utils import make_hashid


# Create your models here.
class Users(AbstractUser):
    GENDER_M = 'M'
    GENDER_F = 'F'
    GENDER_N = 'N'
    GENDERS_CHOICE = [
        (GENDER_M, 'Men'),
        (GENDER_F, 'Female'),
        (GENDER_N, 'Unknown'),
    ]
    uid = models.CharField(max_length=32, unique=True, editable=False, verbose_name="用户ID")
    nickname = models.CharField(max_length=32, blank=True, null=True, default='', verbose_name="昵称")
    gender = models.CharField(max_length=10, choices=GENDERS_CHOICE, default=GENDER_N, verbose_name="性别")
    avatar = models.CharField(max_length=128, blank=True, default='', verbose_name="头像")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "users"
        verbose_name = "用户"
        verbose_name_plural = "用户管理"

    def __str__(self):
        return self.username


class GithubUser(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True)
    gid = models.IntegerField(blank=False, null=False)
    login = models.CharField(max_length=100, blank=True, null=True, default="")
    url = models.URLField(max_length=100, blank=True, null=True, default="")
    avatar_url = models.URLField(max_length=100, blank=True, null=True, default="")
    html_url = models.URLField(max_length=100, blank=True, null=True, default="")
    followers_url = models.URLField(max_length=100, blank=True, null=True, default="")
    following_url = models.URLField(max_length=100, blank=True, null=True, default="")
    gists_url = models.URLField(max_length=100, blank=True, null=True, default="")
    starred_url = models.URLField(max_length=100, blank=True, null=True, default="")
    subscriptions_url = models.URLField(max_length=100, blank=True, null=True, default="")
    organizations_url = models.URLField(max_length=100, blank=True, null=True, default="")
    repos_url = models.URLField(max_length=100, blank=True, null=True, default="")
    events_url = models.URLField(max_length=100, blank=True, null=True, default="")
    received_events_url = models.URLField(max_length=100, blank=True, null=True, default="")
    type = models.CharField(max_length=10, blank=True, null=True, default="")
    site_admin = models.BooleanField(default=False)
    name = models.CharField(max_length=50, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True, default="")
    blog = models.CharField(max_length=50, blank=True, null=True, default="")
    location = models.CharField(max_length=100, blank=True, null=True, default="")
    email = models.EmailField(max_length=128, blank=True, null=True, default="")
    bio = models.CharField(max_length=50, blank=True, null=True, default="")
    twitter_username = models.CharField(max_length=50, blank=True, null=True, default="")
    public_repos = models.IntegerField(blank=True, null=True, default=0)
    public_gists = models.IntegerField(blank=True, null=True, default=0)
    followers = models.IntegerField(blank=True, null=True, default=0)
    following = models.IntegerField(blank=True, null=True, default=0)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'github_user'
        verbose_name = "github用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.login


@receiver(post_save, sender=Users, dispatch_uid='gen_users_uid')
def update_uid(sender, instance, **kwargs):
    if not instance.uid:
        instance.uid = make_hashid(instance.id)  # 生成用户UID
        instance.save()