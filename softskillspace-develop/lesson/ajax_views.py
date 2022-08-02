from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware
from django.views.generic import TemplateView

from lesson.models import Lesson
from softskillspace.utils.choices import LessonStatus


class CalendarJsonView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        params = request.GET.dict()
        _start_date = params.get("start", "")
        _end_date = params.get("end", "")

        start_date = parse_datetime(_start_date)
        if not start_date:
            _start_date = _start_date + " 00:00:00"
            start_date = parse_datetime(_start_date)

        end_date = parse_datetime(_end_date)
        if not end_date:
            _end_date = _end_date + " 00:00:00"
            end_date = parse_datetime(_end_date)

        # get all the booked lessons for the user
        # subjects = get_user_lessons(request.user).values("id")
        query = Q(
            start_datetime__gte=make_aware(start_date),
            end_datetime__lte=make_aware(end_date),
            status=LessonStatus.Approved,
        )

        query &= Q(
            tutor__user_id=request.user.id) | Q(
            student_id=request.user.id)

        schedules = Lesson.items.filter(query).prefetch_related(
            "student", "tutor", "subject"
        )

        data = []
        for schedule in schedules:
            if schedule.tutor.user_id == request.user.id:
                class_name = "bg-primary"
                title = str(schedule.student)

            else:
                class_name = "bg-dark"
                title = str(schedule.tutor)

            data.append(
                {
                    "title": title,
                    "start": str(schedule.start_datetime),
                    "end": str(schedule.end_datetime),
                    "className": class_name,
                    "textColor": "white",
                    "subject": schedule.subject.name,
                }
            )

        return JsonResponse(data, safe=False)
