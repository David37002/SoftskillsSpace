from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.db.models import F, Q
from django.shortcuts import redirect, render
from django.utils.dateformat import format as date_fmt
from django.views.generic import CreateView, ListView

from lesson.models import Lesson
from softskillspace.utils.choices import LessonPaymentStatus, LessonStatus
from softskillspace.utils.query import get_query
from softskillspace.utils.urls import get_url
from student.forms import StudentBookALessonForm
from subject.models import Subject
from tutor.models import Tutor, TutorSubject


class StudentLessonRecord(LoginRequiredMixin, ListView):
    template_name = "student/lesson-record.html"
    model = Lesson
    context_object_name = "lessons"
    paginate_by = 25

    def get_queryset(self):
        request = self.request
        params = request.GET.dict()
        keyword = params.get("search")
        status = params.get("status")

        query = Q(student_id=request.user.id)

        if keyword:
            query &= get_query(
                keyword,
                [
                    "tutor__user__first_name",
                    "tutor__user__last_name",
                    "subject__name",
                ],
            )

        if status:
            if status == LessonStatus.Cancelled:
                query &= Q(status=LessonStatus.Cancelled)
            elif status == "booking-pending":
                query &= Q(status=LessonStatus.Pending)
            else:
                query &= Q(lessonpayment__status__iexact=status)

        lessons = (
            Lesson.items.filter(query)
            .select_related("tutor", "subject", "lessonpayment")
            .order_by("-start_datetime")
        )

        return lessons

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        extra_context = {
            "LessonPaymentStatus": LessonPaymentStatus,
            "LessonStatus": LessonStatus,
        }

        context.update(extra_context)
        return context


class StudentBookALessonView(LoginRequiredMixin, CreateView):
    template_name = "student/book-a-lesson.html"
    form_class = StudentBookALessonForm
    model = Lesson

    def get_form(self, *args, **kwargs):
        user = self.request.user
        form = super().get_form(*args, **kwargs)

        tutor_id = self.kwargs.get("tutor_id")
        if tutor_id:
            tutor_ids = [tutor_id]
            subject_ids = TutorSubject.items.filter(tutor_id=tutor_id)

        else:
            tutor_ids = Lesson.items.filter(
                student__id=user.id, status=LessonStatus.Approved
            ).values_list("tutor_id", flat=True)
            subject_ids = TutorSubject.items.filter(tutor_id=tutor_id)

        tutors = (
            Tutor.items.filter(id__in=tutor_ids)
            .exclude(id=user.id)
            .order_by("user__first_name", "user__last_name")
        )

        subject_ids = set(subject_ids.values_list("subject_id", flat=True))
        subjects = Subject.items.filter(id__in=subject_ids)

        form.fields["tutor"].queryset = tutors
        form.fields["subject"].queryset = subjects

        return form

    def form_valid(self, form):
        request = self.request
        lesson = form.save(commit=False)

        lesson.student = request.user
        lesson.status = LessonStatus.Pending
        lesson.created_by = request.user
        lesson.save()

        messages.success(
            request,
            f"Lesson has been created. Approval is required from {lesson.tutor}",
        )

        lesson_date = date_fmt(lesson.start_datetime, "j M Y, P")
        url = get_url(request, "lesson:detail", args=[lesson.uuid])

        msg_to_tutor = (
            f"Hi {lesson.tutor}\n\n" +
            f"{lesson.student} has booked in a lesson for you on {lesson_date}. " +
            f"Please visit {url} to approve the booking.\n\n" +
            "Kind Regards\n" +
            "Soft Skill Space team")

        send_mail(
            subject="Soft Skill Space - New lesson booking request",
            message=msg_to_tutor,
            fail_silently=True,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[lesson.tutor.user.email],
        )

        msg_to_student = (
            f"Hi {lesson.student}\n\n" +
            f"Your lesson has been successfully booked with {lesson.tutor} for {lesson_date} " +
            f"Please visit {url} to approve the booking.\n\n" +
            "Kind Regards\n" +
            "Soft Skill Space team")

        send_mail(
            subject="Soft Skill Space - New lesson booking request",
            message=msg_to_student,
            fail_silently=True,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[lesson.student.email],
        )

        return redirect("lesson:detail", uuid=lesson.uuid)
