import uuid

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.db.models import F, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.safestring import SafeString
from django.views.generic import DetailView, ListView, View

from chat.models import Chat, Message
from softskillspace.utils.urls import get_url
from tutor.models import Tutor


class ChatView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    template_name = "chat/detail.html"
    context_object_name = "chat"
    model = Chat
    slug = "uuid"

    def get_object(self):
        uuid = self.kwargs.get("uuid")
        tutor = get_object_or_404(Chat, uuid=uuid)
        return tutor

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chat = self.get_object()
        user = self.request.user
        participant = (chat.participants.all().exclude(
            id=user.id).select_related("tutor").first())

        chat_messages = (
            Message.items.filter(chat=chat).select_related("chat", "sender")
        ).order_by("-id")[:100:-1]

        online = participant.last_login + \
            timezone.timedelta(minutes=5) > timezone.now()

        messages = Message.items.filter(chat=chat).exclude(sender_id=user.id)

        if messages:
            messages.update(read=True)

        extra_context = {
            "participant": participant,
            "online": online,
            "chat_messages": chat_messages,
        }

        context.update(extra_context)
        return context

    def test_func(self):
        user = self.request.user
        chat = self.get_object()
        return user in chat.participants.all()


class CreateChatView(LoginRequiredMixin, View):
    def post(self, request, **kwargs):
        data = request.POST.dict()
        tutor_user_id = data.get("tutor_user_id")
        user_ids = [tutor_user_id, request.user.id]

        query = Q(participants__id__in=user_ids)
        chat = Chat.items.filter(query).first()

        if not chat:
            chat = Chat.objects.create(
                uuid=uuid.uuid4(),
            )
            chat.participants.set(user_ids)
            tutor = Tutor.items.get(id=tutor_user_id)
            url = get_url(request, "chat:detail", [chat.uuid])

            msg = (
                f"Hi {tutor}\n\n" +
                f"You have just received a new message from {request.user}. " +
                f"Please <a href='{url}'>click here</a> to read the message\n\n" +
                "Kind Regards\n" +
                "Soft Skill Space team.")

            msg = SafeString(msg)

            send_mail(
                subject="Soft Skill Space - New message received",
                msg=msg,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[tutor.user.email],
                fail_silently=True,
            )

            messages.success(request, "Chat has been created")

        return redirect("chat:detail", uuid=chat.uuid)


class SendMessageView(LoginRequiredMixin, UserPassesTestMixin, View):
    def post(self, request, **kwargs):
        chat_uuid = kwargs.get("uuid")
        chat = Chat.items.get(uuid=chat_uuid)

        data = request.POST.dict()
        message = data.get("message")

        if message:
            Message.objects.create(
                chat=chat,
                sender=request.user,
                text=message,
            )

            messages = Message.items.filter(chat=chat).exclude(
                sender_id=request.user.id
            )

            if messages:
                messages.update(read=True)

        return redirect("chat:detail", uuid=chat.uuid)

    def test_func(self):
        user = self.request.user
        chat_uuid = self.kwargs.get("uuid")
        chat = Chat.items.get(uuid=chat_uuid)
        return user in chat.participants.all()


class ChatListView(LoginRequiredMixin, ListView):
    template_name = "chat/list.html"
    model = Chat
    context_object_name = "chats"
    paginate_by = 25

    def get_queryset(self):
        user = self.request.user
        chats = (
            Chat.items.filter(participants__id__in=[user.id])
            .prefetch_related("participants")
            .order_by("-updated_at")
            .distinct()
        )

        return chats
