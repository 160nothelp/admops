from django.db import models


class Items(models.Model):
    item_name = models.CharField(max_length=16, verbose_name='项目名', unique=True)

    class Meta:
        verbose_name = "项目"


class ItemPlans(models.Model):
    plan_name = models.CharField(max_length=16, verbose_name='计划名', unique=True)
    item = models.ForeignKey('Items', on_delete=models.CASCADE, related_name='items')

    class Meta:
        verbose_name = '项目计划'
