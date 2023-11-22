from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Discussion(models.Model):

    CohicesRate = [
        ("1", "Poor",),
        ("2", "Fair",),
        ("3", "Good",),
        ("4", "Very Good",),
        ("5", "Perfect",),
    ]

    ImportanceRate = [
        ("1", "Not Important",),
        ("2", "Slightly Important",),
        ("3", "Moderately Important"),
        ("4", "Important"),
        ("5", "Very Important"),
    ]
    topic = models.CharField(max_length=100, null=False, blank=False)
    start_time = models.DateTimeField(auto_now_add=True)
    degree_of_importance = models.CharField(choices=ImportanceRate, null=False)
    rate = models.CharField(max_length=1, choices=CohicesRate)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="discussion_opened")
    is_answered = models.BooleanField(default=False)
    is_terminated = models.BooleanField(default=False)

    class Meta:
        ordering = ("-start_time",)

    def set_is_answered_vlaue(self, user):
        """ this fuction runs when a new ticket created and set if the discussion is answerd by staff
            if user creates a tick to discussion then this discussion is not answered by staff
            elif staff create a tick to discussion then this discussion is answerd by staff """
        if user.is_staff:
            self.is_answered = True
        else:
            self.is_answered = False
        self.save()


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets", null=False)
    sent_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(null=False)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name="tickets", null=False)

    class Meta:
        ordering = ("-sent_date",)