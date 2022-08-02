from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView, UpdateView
from django.views.generic import DetailView, ListView
from career.models import *
from career.forms import Candidateform
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

# Create your views here.

class CareerPage(ListView):
    model = Career
    template_name = "career-template/list.html"
    context_object_name = "careers"
    paginate_by = 3

class CareerDetail(DetailView):
    model = Career
    context_object_name = "careerd"
    template_name = "career-template/detail.html"

class CandidateFormView(LoginRequiredMixin, TemplateView):
    template_name = "career-template/candidate-form-info.html"

    def get(self, request, *args, **kwargs):
        form = Candidateform()


        context = {"form": form}

        return render(request, self.template_name, context)
    def post(self, request, *args, **kwargs):
        form = Candidateform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Request has been sent to Soft Skill Space, "
            )

            return redirect("career:career-page")
        context = {"form": form}
        return render(request, self.template_name, context)
