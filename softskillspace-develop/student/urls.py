from django.urls import path

from student import views

app_name = "student"

urlpatterns = [
    path(
        "lessons/",
        view=views.StudentLessonRecord.as_view(),
        name="lesson-record",
    ),
    path(
        "book-a-lesson/<int:tutor_id>/",
        view=views.StudentBookALessonView.as_view(),
        name="book-a-lesson",
    ),
    path(
        "book-a-lesson/",
        view=views.StudentBookALessonView.as_view(),
        name="book-a-lesson",
    ),
]
