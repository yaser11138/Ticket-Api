from rest_framework import serializers
from .models import Ticket, Discussion
from accounts.serializers import UserSerializer


class TicketSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = "__all__"
        extra_kwargs = {
            "discussion": {"read_only": True},
        }
#        ordering = ('sent_date', "id",)


class DiscussionSerializer(serializers.ModelSerializer):
    
    #tickets = TicketSerializer(many=True, read_only=True)
    tickets = serializers.SerializerMethodField()

    class Meta:
        model = Discussion
        fields = "__all__"
        extra_kwargs = {
            "user": {"read_only": True},
            "rate": {"read_only": True},
            "is_terminated": {"read_only": True},
            "is_answered": {"read_only": True}
        }

    def get_tickets(self, instance):
        tickets = instance.tickets.all().order_by("sent_date")
        tickets_data = TicketSerializer(tickets, many=True).data
        return tickets_data  

class DiscussionListSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Discussion
        fields = ("id", "start_time", "user_username", "topic", "degree_of_importance", "is_terminated", "is_answered", "department")


class CombinedDiscussionTicketSerializer(serializers.Serializer):
    discussion = DiscussionSerializer()
    ticket = TicketSerializer()

    def create(self, validated_data):
        # Extract discussion and ticket data
        discussion_data = validated_data['discussion']
        ticket_data = validated_data['ticket']
        user = validated_data["user"]
        discussion_instance = Discussion.objects.create(user=user, **discussion_data)
        ticket_instacnce = Ticket.objects.create(user=user, discussion=discussion_instance, **ticket_data)

        return {'discussion': discussion_instance, "ticket": ticket_instacnce}
