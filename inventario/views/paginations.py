from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'items': self.page.paginator.count,
            'status': 'ok',
            'page': f'{self.page.number}/{self.page.paginator.num_pages}',
            'data': data
        }, status=status.HTTP_200_OK)