from django.urls import path
from .views import OpenDiscussion

urlpatterns = [
    path("open-discussion/", OpenDiscussion.as_view(), name="open-discussion"),
]
