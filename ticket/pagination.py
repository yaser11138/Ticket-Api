from rest_framework.pagination import PageNumberPagination


class DiscussionPagination(PageNumberPagination):
    page_size = 10
