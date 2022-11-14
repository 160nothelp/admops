from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    class Meta:
        db_table = "auth_user" # 保持原来名字，方便使用
        verbose_name = "用户详细信息"
    phone = models.CharField(max_length=32, verbose_name='电话号码', null=True, blank=True)
