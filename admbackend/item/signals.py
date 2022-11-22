from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from .models import Items


@receiver(post_save, sender=Items)
def create_items_permission(sender, instance, created, **kwargs):
    model_name = Items.__name__
    content_type = ContentType.objects.get_for_model(Items)
    # created:新建数据时是True,更新是False
    Permission.objects.update_or_create(
        codename=f'view_{model_name}_{instance.id}',
        content_type=content_type,
        defaults={'name': f'Can view {model_name} {instance.item_name}'},
    )


@receiver(post_delete, sender=Items)
def delete_items_permission(sender, instance, **kwargs):
    model_name = Items.__name__
    content_type = ContentType.objects.get_for_model(Items)
    perms = Permission.objects.get(
        codename=f'view_{model_name}_{instance.id}',
        name=f'Can view {model_name} {instance.item_name}',
        content_type=content_type,
    )
    perms.delete()
