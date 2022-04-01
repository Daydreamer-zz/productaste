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
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "users"
        verbose_name = "用户"
        verbose_name_plural = "用户管理"

    def __str__(self):
        return self.username


class GithubUser(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True)
    gid = models.CharField(max_length=50, editable=False)
    login = models.CharField(max_length=200)
    name = models.CharField(max_length=200, blank=True, null=True, default='')
    email = models.CharField(max_length=120, blank=True, null=True, default='')
    bio = models.CharField(max_length=200, blank=True, null=True, default='')
    location = models.CharField(max_length=200, blank=True, null=True, default='')
    repo_url = models.URLField()
    avatar_url = models.URLField()
    followers_url = models.URLField()
    subscriptions_url = models.URLField()
    html_url = models.URLField()
    organizations = models.URLField()
    public_gists = models.IntegerField(default=0)
    followers = models.IntegerField(default=0)
    public_repos = models.IntegerField(default=0)
    create_at = models.CharField(max_length=20)
    update_at = models.CharField(max_length=20)

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