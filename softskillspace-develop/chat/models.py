import uuid

import auto_prefetch
from django.db import models
from django.template.defaultfilters import truncatechars
from django.utils.dateformat import format as date_fmt
from django.utils.functional import cached_property

from softskillspace.utils.models import TimeBasedModel


class Chat(TimeBasedModel):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    participants = models.ManyToManyField("home.CustomUser", blank=True)

    def __str__(self):
        return f"Chat #{self.id}"

    @cached_property
    def members(self):
        """
        List usernames of all members of a chat
        """
        return ", ".join(self.participants.values_list("username", flat=True))


class Message(TimeBasedModel):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    chat = models.ForeignKey(
        "chat.Chat", null=True, blank=True, on_delete=models.SET_NULL
    )

    sender = auto_prefetch.ForeignKey(
        "home.CustomUser", on_delete=models.CASCADE)
    text = models.TextField(max_length=400, blank=True, null=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return self.preview

    @property
    def preview(self):
        """
        Limit text characters for previewing
        """
        return truncatechars(self.text, 50)

    def created_date(self):
        """
        Format the created at date in the default django way
        """
        date_time = date_fmt(self.created_at, "j M Y, P")
        return date_time
