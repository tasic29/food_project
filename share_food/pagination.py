from rest_framework.pagination import PageNumberPagination


class Defaultpagination(PageNumberPagination):
    page_size = 10
