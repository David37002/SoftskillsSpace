from django.urls import path

# from career import ajax_views
from career import views as career_view

app_name = "career"


urlpatterns = [
    path("",career_view.CareerPage.as_view(),name="career-page"),
    path("<int:pk>/", career_view.CareerDetail.as_view(), name="careerdetail"),
    path("fillform/", career_view.CandidateFormView.as_view(), name="candidateformview")


]
