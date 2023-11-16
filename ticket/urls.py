from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import DiscussionTicketViewSet, CreateTask

urlpatterns = [
    path("create-ticket/", CreateTask.as_view(), name="create-ticket"),
]

router = DefaultRouter()
router.register(r'discussion', DiscussionTicketViewSet, basename='discussion')
urlpatterns += router.urls
