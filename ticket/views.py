from django.db import transaction
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import CombinedDiscussionTicketSerializer, TicketSerializer, DiscussionSerializer
from .models import Discussion
from .pagination import DiscussionPagination
from .permissions import IsnotStaff, IsOwnerOrStuff


class DiscussionTicketViewSet(viewsets.ViewSet, DiscussionPagination):
    def get_permissions(self):
        if self.action == 'create' or self.action == 'rate':
            permission_classes = [IsAuthenticated, IsnotStaff]
        elif self.action == "retrive":
            permission_classes = [IsAuthenticated, IsOwnerOrStuff]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    serializer_class = CombinedDiscussionTicketSerializer

    @transaction.atomic()
    def create(self, request):
        combined_serializer = CombinedDiscussionTicketSerializer(data=request.data)
        if combined_serializer.is_valid():
            combined_serializer.validated_data["user"] = request.user
            data = combined_serializer.save()
            discussion = data["discussion"]
            return Response(data={"status": "Discussion Opened", "data": combined_serializer.data},
                            status=status.HTTP_201_CREATED)
        else:
            return Response(data=combined_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        if request.user.is_staff:
            queryset = Discussion.objects.all()
        else:
            queryset = Discussion.objects.filter(created_by=request.user)
        data = self.paginate_queryset(queryset, request)
        serializer = DiscussionSerializer(instance=data, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            discussion = Discussion.objects.get(pk=pk)
        except Discussion.DoesNotExist:
            return Response(data={"detail": "Discussion not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = DiscussionSerializer(discussion)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def rate(self, request, pk=None):
        if 'rate' not in request.data:
            return Response(data={"error": "Rate hasn't been sent"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            discussion = Discussion.objects.get(pk=pk)
        except Discussion.DoesNotExist:
            return Response(data={"detail": "Discussion not found"}, status=status.HTTP_404_NOT_FOUND)
        discussion.rate = request.data.get("rate")
        discussion.save()
        return Response(data={"detail": "The discussion rated"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        try:
            discussion = Discussion.objects.get(pk=pk)
        except Discussion.DoesNotExist:
            return Response(data={"detail": "Discussion not found"}, status=status.HTTP_404_NOT_FOUND)
        discussion.is_terminated = True
        discussion.save()
        return Response(data={"detail": "The discussion closed"}, status=status.HTTP_200_OK)


class CreateTicket(APIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, discussion_id):
        discussion = Discussion.objects.get(id=discussion_id)
        ticket_serializer = TicketSerializer(data=request.data)
        if ticket_serializer.is_valid():
            ticket_serializer.validated_data["discussion"] = discussion
            ticket_serializer.validated_data["user"] = request.user
            ticket_serializer.save()
            discussion.set_is_answered_vlaue(request.user)
            return Response(data={"ticket": ticket_serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={"error": ticket_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
