from django.urls import path

from tutor import ajax_views, views

app_name = "tutor"

urlpatterns = [
    path("search/", view=views.SearchView.as_view(), name="search"),
    path(
        "<str:username>/profile/",
        view=views.TutorProfileView.as_view(),
        name="profile",
    ),
    path(
        "profile/edit/",
        view=views.TutorProfileUpdateView.as_view(),
        name="edit-tutor",
    ),
    path(
        "lessons/",
        view=views.TutorLessonRecord.as_view(),
        name="lesson-record",
    ),
    path(
        "book-a-lesson/<int:student_id>/",
        view=views.TutorBookALessonView.as_view(),
        name="book-a-lesson",
    ),
    path(
        "book-a-lesson/",
        view=views.TutorBookALessonView.as_view(),
        name="book-a-lesson",
    ),
    path(
        "availability/",
        view=views.TutorAvailabilityView.as_view(),
        name="availability",
    ),
    path(
        "qualifications/",
        view=views.QualificationsView.as_view(),
        name="qualifications",
    ),
    # AJAX
    path(
        "<str:id>/rate-per-hour.json",
        view=ajax_views.GetTutorRatePerHour.as_view(),
        name="rate-per-hour-json",
    ),
    path(
        "delete/",
        view=views.QualificationsDeleteView.as_view(),
        name="qualification-delete",
    ),
]
