from django.urls import path

from home import ajax_views
from home import views as home_view

app_name = "home"

urlpatterns = [
    path(
        "about-us/",
        view=home_view.AboutUsView.as_view(),
        name="about-us",
    ),
    path(
        "accounts/profile/update/",
        view=home_view.ProfileUpdateView.as_view(),
        name="edit-profile",
    ),
    path(
        "coming-soon/",
        view=home_view.ComingSoonView.as_view(),
        name="coming-soon"),
    path(
        "dashboard/",
        view=home_view.DashboardView.as_view(),
        name="dashboard"),
    path(
        "accounts/profile/remove-image/",
        view=ajax_views.RemoveImageView.as_view(),
        name="remove-image",
    ),
    path(
        "accounts/profile/change-country-data/",
        view=ajax_views.ChangeCountryDataView.as_view(),
        name="change-country-data",
    ),
    path(
        "accounts/profile/update-image/",
        view=ajax_views.UpdateImageView.as_view(),
        name="update-image",
    ),
    path(
        "",
        view=home_view.IndexView.as_view(),
        name="index"),
    path(
        "become-a-tutor/",
        home_view.BecomeATutorView.as_view(),
        name="become-a-tutor"),
    path(
        "contact-us/",
        home_view.ContactUsView.as_view(),
        name="contact-us"),
    path(
        "terms-of-use/",
        home_view.TermsOfUseView.as_view(),
        name="terms-of-use"),

    
]
