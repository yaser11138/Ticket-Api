from django.db import transaction
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .serializers import CombinedDiscussionTicketSerializer, TicketSerializer, DiscussionSerializer
from .models import Discussion


class DiscussionTicketViewSet(viewsets.ViewSet):
    serializer_class = CombinedDiscussionTicketSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic()
    def create(self, request):
        combined_serializer = CombinedDiscussionTicketSerializer(data=request.data)
        if combined_serializer.is_valid():
            combined_serializer.validated_data["user"] = request.user
            combined_serializer.save()

            return Response(data={"status": "Discussion Opened", "data": combined_serializer.data},
                            status=status.HTTP_201_CREATED)
        else:
            return Response(data=combined_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        discussions = Discussion.objects.all()
        serializer = DiscussionSerializer(discussions, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            discussion = Discussion.objects.get(pk=pk)
        except Discussion.DoesNotExist:
            return Response(data={"detail": "Discussion not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = DiscussionSerializer(discussion)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], name="rate")
    def rate(self, request, pk=None):
        try:
            discussion = Discussion.objects.get(pk=pk)
        except Discussion.DoesNotExist:
            return Response(data={"detail": "Discussion not found"}, status=status.HTTP_404_NOT_FOUND)
        if request.data.get("rate") is None:
            return Response(data={"error": "rate haven't sent"})
        else:
            discussion.rate = request.data.get("rate")
            discussion.is_terminated = True
            discussion.save()
            return Response(data={"detail": "The discussion was rated"})


class CreateTask(APIView):
    serializer_class = TicketSerializer

    def post(self, request, discussion_id):
        discussion = Discussion.objects.get(id=discussion_id)
        ticket_serializer = TicketSerializer(data=request.data)
        if ticket_serializer.is_valid():
            ticket_serializer.validated_data["discussion"] = discussion
            ticket_serializer.validated_data["user"] = requset.user
            ticket_serializer.save()
            return Response(data={"ticket": ticket_serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={"error": ticket_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

