from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from .models import Items, ItemPlans
from .serializers import ItemsSerializer, ItemPlansSerializer
from utils.exceptions import NotFound, ValidationError
from .permissions import ItemsPermission


class ItemsViewSet(ModelViewSet):
    queryset = Items.objects.all()
    serializer_class = ItemsSerializer


class ItemPlansViewSet(ModelViewSet):
    queryset = ItemPlans.objects.all()
    serializer_class = ItemPlansSerializer
    permission_classes = (ItemsPermission,)

    def get_queryset(self):
        try:
            item_name = self.request.query_params.get('item_name').split(',')
        except Exception:
            raise ValidationError
        if item_name is None:
            raise NotFound
        queryset = self.queryset.filter(item_id__in=item_name)
        return queryset

    @action(['GET'], detail=False, url_path='items')
    def items(self, request):
        if request.user.is_superuser:
            return Response(list(ItemsViewSet.queryset.all().values('id', 'item_name').order_by('id')))
        content_type = ContentType.objects.get_for_model(Items)
        perms_queryset = Permission.objects.filter(group__user=request.user, content_type=content_type).values('codename')
        item_id_list = [i.get('codename').split('_')[-1] for i in perms_queryset
                        if i.get('codename').split('_')[-1].isdigit()]
        return Response(list(ItemsViewSet.queryset.filter(pk__in=item_id_list).values('id', 'item_name').order_by('id')))

