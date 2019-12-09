from rest_framework.pagination import PageNumberPagination

class RssItemResultsSetPagination(PageNumberPagination):
    page_size_query_param = 'pageSize'