from django.urls import path

from lesson import ajax_views, views

app_name = "lesson"

urlpatterns = [
    path(
        "calendar/",
        view=views.CalendarView.as_view(),
        name="calendar"),
    path(
        "<uuid:uuid>/detail/",
        view=views.LessonDetailView.as_view(),
        name="detail"),
    path(
        "calendar.json",
        view=ajax_views.CalendarJsonView.as_view(),
        name="calendar-json",
    ),
    path(
        "<uuid:uuid>/payment/",
        view=views.LessonPaymentView.as_view(),
        name="payment",
    ),
    path(
        "<uuid:uuid>/give-review/",
        view=views.LessonTutorRatingView.as_view(),
        name="give-review",
    ),
    path(
        "<uuid:uuid>/decline-booking/",
        view=views.DeclineBookingView.as_view(),
        name="decline-booking",
    ),
]
