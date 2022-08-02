from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.db.models import Avg, Count, F, Q, Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.dateformat import format as date_fmt
from django.views import View
from django.views.generic import (CreateView, DetailView, FormView, ListView,
                                  UpdateView)
from requests import request

from home.models import CustomUser
from lesson.models import Lesson, Review
from softskillspace.utils.choices import AcademicLevel, InstitutionType, LessonPaymentStatus, LessonStatus
from softskillspace.utils.html import rating_to_html
from softskillspace.utils.misc import AvailabilityHandler
from softskillspace.utils.query import get_query
from softskillspace.utils.urls import get_url
from subject.models import Subject
from tutor.forms import TutorAvailabilityForm, TutorBookALessonForm, TutorForm, TutorQualificationForm
from tutor.models import (Tutor, TutorAvailability, TutorQualification,
                          TutorSubject)


class SearchView(ListView):
    template_name = "tutor/search.html"
    context_object_name = "tutors"
    paginate_by = 20
    model = Tutor
    allow_empty = True

    def get_queryset(self):
        query = Q(
            verified_at__isnull=False,
            verified_at__lte=timezone.now(),
        )

        params = self.request.GET.dict()
        keyword = params.get("keyword")
        sortby = params.get("sortby")

        if keyword:
            search_fields = [
                "tutorsubject__subject__name",
                "tutorsubject__subject__categories__name",
                "tutorsubject__subject__subcategories",
            ]

            query &= get_query(keyword, search_fields)

        date_filter = Q(
            lesson__end_datetime__lte=timezone.now(),
            lesson__status=LessonStatus.Approved,
        )

        tutors = (
            Tutor.items.filter(query)
            .select_related("user")
            .annotate(
                hours_taught=Sum(
                    F("lesson__duration_minutes") / 60.0, filter=date_filter
                ),
                average_review=Avg(
                    F("lesson__review__rating"),
                    default=0,
                    filter=Q(lesson__review__isnull=False) & date_filter,
                    distinct=True,
                ),
            )
            .prefetch_related("lesson_set")
        )

        ordering_map = {
            "rate-per-hour": "rate_per_hour",
            "hours-taught": "-hours_taught",
            "ratings": "-average_review",
        }

        sort_value = ordering_map.get(sortby)

        if sort_value:
            tutors = tutors.order_by(sort_value)

        return tutors

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        params = self.request.GET.dict()

        context.update(params)
        return context


class DashboardView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    context_object_name = "tutor"
    template_name = "tutor/dashboard.html"
    model = Tutor

    def test_func(self):
        return self.request.user.is_tutor

    def handle_no_permission(self):
        messages.error(self.request, "You are not a Tutor.")
        return redirect("home:index")


class TutorProfileView(DetailView):
    template_name = "tutor/profile.html"
    model = Tutor
    context_object_name = "tutor"
    slug = "username"

    def get_object(self):
        username = self.kwargs.get("username")
        tutor = get_object_or_404(Tutor, user__username__iexact=username)
        return tutor

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tutor = self.object

        tutor_stat = (
            Lesson.items.filter(
                tutor=tutor,
                status=LessonStatus.Approved,
                end_datetime__lte=timezone.now(),
            ) .select_related(
                "tutor",
                "review") .aggregate(
                hours_taught=Sum(
                    F("duration_minutes") /
                    60,
                    distinct=True,
                    default=0),
                total_reviews=Count(
                    F("review")),
                average_rating=(
                    Avg("review__rating")),
            ))

        reviews = (
            Review.items.filter(lesson__tutor_id=tutor.id)
            .order_by("-created_at")
            .select_related("lesson__student")[:5]
        )

        subjects = (
            TutorSubject.items.filter(tutor=tutor)
            .order_by("subject__name")
            .select_related("subject")
        )

        average_rating = tutor_stat["average_rating"]
        star_rating = rating_to_html(average_rating)

        extra_context = {
            "tutor_stat": tutor_stat,
            "star_rating": star_rating,
            "subjects": subjects,
            "reviews": reviews,
        }

        context.update(extra_context)
        return context


class TutorLessonRecord(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = "tutor/lesson-record.html"
    model = Lesson
    context_object_name = "lessons"
    paginate_by = 25

    def get_queryset(self):
        request = self.request
        params = request.GET.dict()
        keyword = params.get("search")
        status = params.get("status")

        query = Q(tutor__user_id=request.user.id)

        if keyword:
            query &= get_query(
                keyword,
                [
                    "student__first_name",
                    "student__last_name",
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
            .select_related("student", "subject", "lessonpayment")
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

    def test_func(self):
        return self.request.user.is_tutor


class TutorBookALessonView(
        LoginRequiredMixin,
        UserPassesTestMixin,
        CreateView):
    template_name = "tutor/book-a-lesson.html"
    form_class = TutorBookALessonForm
    model = Lesson

    def get_form(self, *args, **kwargs):
        user = self.request.user
        form = super().get_form(*args, **kwargs)

        student_ids = Lesson.items.filter(
            tutor__user_id=user.id, status=LessonStatus.Approved
        ).values_list("student_id", flat=True)

        students = (
            CustomUser.items.filter(id__in=student_ids)
            .exclude(id=user.id)
            .order_by("first_name", "last_name")
        )

        subject_ids = TutorSubject.items.filter(tutor_id=user.tutor.id)

        subject_ids = set(subject_ids.values_list("subject_id", flat=True))
        subjects = Subject.items.filter(id__in=subject_ids)

        form.fields["student"].queryset = students
        form.fields["subject"].queryset = subjects

        form.fields[
            "price_per_hour"
        ].label = f"Price per hour (Default {user.tutor.rate_per_hour})"
        form.fields["price_per_hour"].initial = user.tutor.rate_per_hour

        return form

    def form_valid(self, form):
        request = self.request
        lesson = form.save(commit=False)

        lesson.tutor = request.user.tutor
        lesson.status = LessonStatus.Pending
        lesson.created_by = request.user
        lesson.save()

        messages.success(
            request,
            f"Lesson has been created. Approval is required from {lesson.student}",
        )

        lesson_date = date_fmt(lesson.start_datetime, "j M Y, P")
        url = get_url(request, "lesson:detail", args=[lesson.uuid])

        msg_to_student = (
            f"Hi {lesson.student}\n\n" +
            f"{lesson.tutor} has booked in a lesson for you on {lesson_date}.\n" +
            f"Please visit {url} for more information.")

        send_mail(
            subject="Soft Skill Space - New lesson booking request",
            message=msg_to_student,
            fail_silently=True,
            from_email=lesson.tutor.user.email,
            recipient_list=[lesson.student.email],
        )

        return redirect("lesson:detail", uuid=lesson.uuid)

    def test_func(self):
        return self.request.user.is_tutor


class TutorProfileUpdateView(
        LoginRequiredMixin,
        UserPassesTestMixin,
        UpdateView):
    template_name = "tutor/edit-tutor-profile.html"
    form_class = TutorForm

    def get_object(self):
        return self.request.user.tutor

    def get_success_url(self):
        url = reverse("tutor:edit-tutor")
        messages.success(
            self.request,
            "Your profile has been updated successfully")
        return url

    def test_func(self):
        user = self.request.user
        return user.is_tutor


class TutorAvailabilityView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = "tutor/availability.html"
    form_class = TutorAvailabilityForm

    def get_initial(self):
        availability, _ = TutorAvailability.objects.get_or_create(
            tutor=self.request.user.tutor
        )

        handler = AvailabilityHandler(availability)
        initials = handler.get_availability_data()
        return initials

    def form_valid(self, form):
        data = form.cleaned_data

        availability, _ = TutorAvailability.objects.get_or_create(
            tutor=self.request.user.tutor
        )

        handler = AvailabilityHandler(availability)
        handler.set_availability_data(data)
        messages.success(self.request, "Availability updated")
        return redirect(self.request.path_info)

    def test_func(self):
        return self.request.user.is_tutor


class QualificationsView(LoginRequiredMixin, UserPassesTestMixin, ListView, FormView):
    template_name = "tutor/qualifications.html"
    context_object_name = "qualifications"
    paginate_by = 25
    model = TutorQualification
    form_class = TutorQualificationForm
    success_url = reverse_lazy("tutor:qualifications")

    def get_initial(self):
        initial = super().get_initial()
        initial.update({
            "institution_type": InstitutionType.University,
            "level": AcademicLevel.Degree,
        })
        return initial

    def get_queryset(self):
        qualifications = TutorQualification.items.filter(
            tutor__user_id=self.request.user.id
        ).order_by("-end_date", "-start_date")

        return qualifications

    def test_func(self):
        return self.request.user.is_tutor

    def form_valid(self, form):
        request = self.request
        qual = form.save(commit=False)
        qual.tutor = request.user.tutor
        qual.save()

        messages.success(request, "New qualification successfully added")
        return redirect(self.success_url)


class QualificationsDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    def post(self, request, *args, **kwargs):
        id = request.POST.get("id")
        success = False
        message = "Qualification could not be deleted"

        quals = TutorQualification.items.filter(
            id=id, tutor__user=self.request.user
        )

        if quals:
            quals.delete()
            success = True
            message = "Qualification successfully deleted"

        data = {
            "success": success,
            "msg": message
        }

        return JsonResponse(data)

    def test_func(self):
        return self.request.user.is_tutor
