import time
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from utils.id_utils import make_hashid
from apps.account.models import Users


# Create your models here.
class Product(models.Model):
    pid = models.CharField(max_length=32, unique=True, editable=False, verbose_name="产品ID")
    name = models.CharField(max_length=100, verbose_name="产品名称")
    url = models.URLField(verbose_name="产品链接")
    digest = models.CharField(max_length=100, verbose_name="产品描述")
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name="用户")
    vote_count = models.IntegerField(default=0, verbose_name="点赞数")
    public = models.BooleanField(default=True, verbose_name="是否显示")
    remark = models.CharField(max_length=100, default="", null=True, verbose_name="备注")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "products"
        verbose_name = "产品"
        verbose_name_plural = "产品管理"

    def __str__(self):
        return self.name

    def vote(self, user):
        p_vote = ProductVoteUser()
        p_vote.user = user
        p_vote.product = self
        p_vote.add_time = int(time.time())
        p_vote.save()
        self.vote_count += 1
        self.save(update_fields=["vote_count"])


class ProductVoteUser(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    add_time = models.IntegerField(default=0)

    class Meta:
        db_table = "product_vote"
        verbose_name = "产品点赞"
        verbose_name_plural = "产品点赞管理"


@receiver(signal=post_save, sender=Product, dispatch_uid="gen_product_id")
def update_pid(sender, instance, **kwargs):
    if not instance.pid:
        instance.pid = make_hashid(instance.id, 8)
        instance.save()