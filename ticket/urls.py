from django.urls import path
from .views import OpenDiscussion,CreateTask

urlpatterns = [
    path("open-discussion/", OpenDiscussion.as_view(), name="open-discussion"),
    path("create-ticket/", CreateTask.as_view(), name="create-ticket"),
]
