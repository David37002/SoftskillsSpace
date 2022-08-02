from django.urls import path

from chat import views

app_name = "chat"

urlpatterns = [
    path(
        "<uuid:uuid>/",
        view=views.ChatView.as_view(),
        name="detail"),
    path(
        "create-chat/",
        view=views.CreateChatView.as_view(),
        name="create-chat"),
    path(
        "send-message/<uuid:uuid>/",
        view=views.SendMessageView.as_view(),
        name="send-message",
    ),
    path(
        "list/",
        view=views.ChatListView.as_view(),
        name="list",
    ),
]
