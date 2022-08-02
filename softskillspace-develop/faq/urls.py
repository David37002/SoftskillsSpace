from django.urls import path

from faq import views

app_name = "faq"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
]
