from django.conf import settings
from django.db.models import Avg, Count, Q
from django.utils import timezone

from lesson.models import Lesson
from softskillspace.utils.choices import LessonPaymentStatus, LessonStatus


def page_data_filter(request):
    """
    Globally available variables
    """

    namespace = request.resolver_match.namespace
    is_instructor_page = namespace in ["instructor"]
    is_tutor_page = namespace in ["tutor"]

    context = {
        "is_instructor_page": is_instructor_page,
        "is_tutor_page": is_tutor_page,
    }

    if len(settings.GOOGLE_ANALYTICS_ID) > 1:
        context.update({"GOOGLE_ANALYTICS_ID": settings.GOOGLE_ANALYTICS_ID})

    return context


def user_stats(request):
    """
    Displays general statistical information on the dashboard
    """

    user = request.user
    context = {}

    if not user.is_authenticated:
        return context

    if user.is_tutor:
        lesson_filter = Q(
            status=LessonStatus.Approved,
            lessonpayment__status=LessonPaymentStatus.Paid,
            end_datetime__gte=timezone.now() + timezone.timedelta(hours=4),
        )

        tutor_stat = Lesson.items.filter(
            lesson_filter,
            tutor__user_id=user.id,
        ).aggregate(
            avg_rating=Avg("review__rating", distinct=True),
            students=Count("student", distinct=True),
            lessons=Count("id", distinct=True),
        )

        context = {
            "tutor_stat": tutor_stat,
        }

    return context
