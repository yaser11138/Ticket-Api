from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import CombinedDiscussionTicketSerializer, TicketSerializer
from .models import Discussion


class OpenDiscussion(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        combined_serializer = CombinedDiscussionTicketSerializer(data=request.data)
        if combined_serializer.is_valid():
            combined_serializer.validated_data["user"] = request.user
            combined_serializer.save()

            return Response(data={"status": "Discussion Opened", "data": combined_serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(data=combined_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateTask(APIView):

    def post(self, request, discussion_id):
        discussion = Discussion.objects.get(id=discussion_id)
        ticket_serializer = TicketSerializer(data=request.data)
        if ticket_serializer.is_valid():
            ticket_serializer.validated_data["discussion"] = discussion
            ticket_serializer.validated_data["user"] = user
            ticket_serializer.save()
            return Response(data={"ticket": ticket_serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={"error": ticket_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

