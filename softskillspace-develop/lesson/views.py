import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView, TemplateView

from lesson.models import Lesson, Review
from payment.models import LessonPayment
from softskillspace.utils.choices import (LessonPaymentStatus, LessonStatus,
                                          PaymentMethodChoice)
from softskillspace.utils.payments import (lesson_payment_with_stripe,
                                           make_free_payment)
from softskillspace.utils.urls import get_url

stripe.api_key = settings.STRIPE_SECRET_KEY


class CalendarView(LoginRequiredMixin, TemplateView):
    template_name = "lesson/calendar.html"


class LessonDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    template_name = "lesson/detail.html"
    model = Lesson
    context_object_name = "lesson"
    slug_url_kwarg = "uuid"
    slug_field = "uuid"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson = self.get_object()

        can_review = (
            lesson.start_datetime +
            timezone.timedelta(
                hours=4) < timezone.now())
        can_review = can_review and not hasattr(lesson, "review")

        extra_context = {
            "LessonPaymentStatus": LessonPaymentStatus,
            "LessonStatus": LessonStatus,
            "can_review": can_review,
        }

        context.update(extra_context)
        return context

    def test_func(self):
        user = self.request.user
        lesson = self.get_object()
        participants_id = [lesson.tutor.user_id, lesson.student_id]
        return user.id in participants_id


class LessonPaymentView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    template_name = "lesson/payment.html"
    model = Lesson
    context_object_name = "lesson"
    slug_url_kwarg = "uuid"
    slug_field = "uuid"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        extra_context = {
            "LessonPaymentStatus": LessonPaymentStatus,
            "stripe_pk": settings.STRIPE_PUBLIC_KEY,
            "PaymentMethodChoice": PaymentMethodChoice,
        }

        context.update(extra_context)
        return context

    def post(self, request, *args, **kwargs):
        contact_error_msg = (
            "Please try a different payment method or contact us at "
            + f"{settings.DEFAULT_FROM_EMAIL}"
        )

        data = request.POST.dict()
        lesson = self.get_object()
        token = data.get("stripeToken")
        payment_method = data.get("payment_method")

        amount = lesson.total_cost

        if amount > 0:
            if payment_method == PaymentMethodChoice.Stripe:
                lesson_payment_with_stripe(
                    request, amount, token, lesson, contact_error_msg
                )
        else:
            make_free_payment(request, lesson)

        return redirect(request.path_info)

    def test_func(self):
        user = self.request.user
        lesson = self.get_object()
        return lesson.student == user


class LessonTutorRatingView(LoginRequiredMixin, UserPassesTestMixin, View):
    def post(self, request, *args, **kwargs):
        lesson_uuid = kwargs.get("uuid")
        lesson = Lesson.items.get(uuid=lesson_uuid)

        data = request.POST.dict()

        comment = data.get("comment")
        rating = data.get("rating")

        if comment and rating:
            Review.objects.create(
                lesson=lesson,
                rating=rating,
                comment=comment)

            messages.success(request, "Your review has been posted")
        else:
            messages.error(request, "Could not post review")

        return redirect("lesson:detail", uuid=lesson.uuid)

    def test_func(self):
        user = self.request.user
        lesson_uuid = self.kwargs.get("uuid")
        lesson = Lesson.items.get(uuid=lesson_uuid)
        return lesson.student == user


class DeclineBookingView(LoginRequiredMixin, UserPassesTestMixin, View):
    def post(self, request, *args, **kwargs):
        lesson_uuid = kwargs.get("uuid")
        lesson = Lesson.items.get(uuid=lesson_uuid)
        lesson.status = LessonStatus.Cancelled
        lesson.save()

        url = get_url(request, "lesson:detail", args=[lesson.uuid])

        msg = (
            f"Booking for {lesson.subject} "
            + f"has been declined by {request.user}\n\n"
            + f"Please visit {url} for more information\n\n"
            + "The Soft Skill Space Team"
        )

        recipient = request.user
        if lesson.student == request.user:
            recipient = lesson.tutor.user
        else:
            recipient = lesson.student

        send_mail(
            subject="Soft Skill Space - Booking declined",
            message=msg,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient.email],
        )
        messages.success(request, "Booking declined")

        return redirect("lesson:detail", uuid=lesson.uuid)

    def test_func(self):
        user = self.request.user
        lesson_uuid = self.kwargs.get("uuid")
        lesson = Lesson.items.get(uuid=lesson_uuid)

        if user.is_tutor:
            return lesson.tutor == user.tutor or lesson.tutor.user_id == user.id
        else:
            return lesson.student_id == user.id
