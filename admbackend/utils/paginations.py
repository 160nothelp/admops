from rest_framework.pagination import PageNumberPagination
from django.core.paginator import InvalidPage
from rest_framework.exceptions import NotFound
from rest_framework.response import Response


class CustomNumberPagination(PageNumberPagination):
    page_size_query_param = 'size'
    max_page_size = 200

    def __init__(self):
        super(CustomNumberPagination, self).__init__()

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        # 重写，把page_size 加到self，很屎的方法
        self.page_size = self.get_page_size(request)
        page_size = self.page_size
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = self.get_page_number(request, paginator)

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=str(exc)
            )
            raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)

    def get_paginated_response(self, data):
        return Response({
            'pagination': {
                'total': self.page.paginator.count,
                'size': self.page_size,
                'page': self.page.number
            },
            'results': data,
        })

