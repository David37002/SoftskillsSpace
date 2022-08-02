from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View

from tutor.models import Tutor


class GetTutorRatePerHour(LoginRequiredMixin, View):
    def get(self, _request, **kwargs):
        """
        Get the rate per hour of the selected tutor
        """

        tutor_id = kwargs.get("id")
        data = {}

        if tutor_id:
            tutor = Tutor.items.filter(id=tutor_id).first()

            if tutor:
                data = {"rate_per_hour": tutor.rate_per_hour}

        return JsonResponse(data, safe=False)
