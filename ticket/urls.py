from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import DiscussionTicketViewSet, CreateTicket

urlpatterns = [
    path("ticket/create/<int:discussion_id>/", CreateTicket.as_view(), name="create-ticket"),
]

router = DefaultRouter()
router.register(r'discussion', DiscussionTicketViewSet, basename='discussion')
urlpatterns += router.urls
