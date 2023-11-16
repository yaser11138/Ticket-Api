from rest_framework import serializers
from .models import Ticket, Discussion
from accounts.serializers import UserSerializer


class TicketSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Ticket
        fields = "__all__"
        extra_kwargs = {
            "discussion": {"read_only": True},
        }


class DiscussionSerializer(serializers.ModelSerializer):

    tickets = serializers.SerializerMethodField()

    class Meta:
        model = Discussion
        fields = "__all__"
        extra_kwargs = {
            "created_by": {"read_only": True},
            "rate": {"read_only": True},
            "is_terminated": {"read_only": True}
        }

    def get_tickets(self, obj):
        tickets = obj.tickets
        tickets_serializer = TicketSerializer(instance=tickets, many=True)
        return tickets_serializer.data


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
