from abc import ABC

from rest_framework import serializers
from .models import Ticket, Discussion


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = "__all__"
        extra_kwargs = {
            "discussion": {"read_only": True},
            "user": {"read_only": True}
        }


class DiscussionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Discussion
        fields = "__all__"
        extra_kwargs = {
            "created_by": {"read_only": True},
            "rate": {"read_only": True}
        }


class CombinedDiscussionTicketSerializer(serializers.Serializer):
    discussion = DiscussionSerializer()
    ticket = TicketSerializer()

    def create(self, validated_data):
        # Extract discussion and ticket data
        discussion_data = validated_data['discussion']
        ticket_data = validated_data['ticket']
        user = validated_data["user"]
        discussion_instance = Discussion.objects.create(created_by=user, **discussion_data)

        ticket_instance = Ticket.objects.create(user=user, discussion=discussion_instance, **ticket_data)

        return {'discussion': discussion_instance, 'ticket': ticket_instance}
