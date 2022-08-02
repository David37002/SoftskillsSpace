from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import View

from location.models import Country


class RemoveImageView(LoginRequiredMixin, View):
    def post(self, request):
        """
        Remove user profile picture through ajax request
        """
        user = request.user
        user.profile_pic = None
        user.save()

        data = {"image_url": user.image_url}
        return JsonResponse(data, safe=False)


class UpdateImageView(LoginRequiredMixin, View):
    def post(self, request):
        """
        update the user profile picture through ajax request
        """
        user = request.user
        profile_pic = request.FILES.get("file")
        success = False
        if profile_pic:
            user.profile_pic = profile_pic
            user.save()
            success = True

        data = {"image_url": user.image_url, "success": success}

        return JsonResponse(data, safe=False)


class ChangeCountryDataView(LoginRequiredMixin, View):
    def post(self, request):
        """
        Get country record via ajax so page can have real time update
        """

        data = {}

        _country = request.POST.get("country")
        if _country:
            country_data = (
                Country.items.filter(id=_country)
                .values("dialling_code", "iso_code")
                .first()
            )

            data.update(country_data)

        return JsonResponse(data, safe=False)
