import re
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db.models import Count, Q
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, TemplateView, UpdateView
from django.views.generic.base import TemplateView, View

from blog.models import Blog
from home.forms import MailingListForm, ProfileUpdateForm
from home.models import CustomUser, MailingList, MailingListCategory
from lesson.models import Lesson
from location.models import Country
from promotion.models import TutorPromotion
from softskillspace.utils.choices import LessonStatus, MailingListType
from softskillspace.utils.settings import get_env_variable
from tutor.forms import TutorRequestForm


class IndexView(TemplateView):
    template_name = "home/index.html"

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        user = request.user
        subscribed_to_newsletter = False
        latest_lesson = None

        if user.is_authenticated:
            user = request.user
            user.last_login = timezone.now()
            user.save()

            subscribed_to_newsletter = MailingList.items.filter(
                email__iexact=user.email,
                categories__name__in=[MailingListType.NewsLetter],
            ).exists()

            lesson_query = Q(
                start_datetime__gte=timezone.now(),
                status=LessonStatus.Approved)

            lesson_query &= Q(tutor__user_id=user.id) | Q(student_id=user.id)

            latest_lesson = (
                Lesson.items.filter(lesson_query)
                .select_related("subject")
                .order_by("start_datetime")
                .first()
            )

        tutor_promos = (
            TutorPromotion.items.filter(
                start_date__lte=timezone.now().date(),
                end_date__gte=timezone.now().date(),
            )
            .annotate(
                lesson_count=Count("tutor__lesson"),
                review_count=Count("tutor__lesson__review"),
            )
            .order_by("end_date")
            .select_related("tutor__user", "tutor")
        )

        blogs = Blog.objects.order_by(
            "-id").select_related("category", "author")[:6]

        extra_context = {
            "tutor_promos": tutor_promos,
            "blogs": blogs,
            "form": MailingListForm(),
            "subscribed_to_newsletter": subscribed_to_newsletter,
            "latest_lesson": latest_lesson,
        }

        context.update(extra_context)
        return render(request, self.template_name, context)

    def post(self, request):
        form = MailingListForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            email = data.get("email")

            mailing_list, _ = MailingList.objects.get_or_create(
                email__iexact=email)
            mail_category, _ = MailingListCategory.items.get_or_create(
                name=MailingListType.NewsLetter
            )
            mailing_list.categories.add(mail_category)

            messages.success(
                self.request,
                "You have been added to our Newsletter 🥂.",
            )
        else:
            messages.error(
                self.request,
                "Email is invalid. Please try again",
            )

        return redirect("home:index")


class ComingSoonView(CreateView):
    template_name = "home/coming-soon.html"
    form_class = MailingListForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        release_date = timezone.datetime(2022, 5, 2).date()
        today = timezone.now().date()
        days_left = (release_date - today).days
        progress = int((34 - days_left) / 0.34)

        context["progress"] = progress
        return context

    def form_valid(self, form):
        mailing_list = form.save(commit=True)
        category, _ = MailingListCategory.objects.get_or_create(
            name=MailingListType.ComingSoon
        )
        mailing_list.categories.add(category)

        messages.success(
            self.request,
            "Thanks for filling the form. You will be notified when the site is ready",
        )

        return redirect("home:index")


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "registration/edit-profile.html"
    model = CustomUser
    form_class = ProfileUpdateForm

    def get_object(self):
        return self.request.user

    def get_form(self, **kwargs):
        form = super().get_form(**kwargs)
        nigeria = Country.items.filter(iso_code__iexact="ng").first()

        form["country"].initial = nigeria
        return form

    def get_success_url(self):
        messages.success(self.request, "Profile updated successfully")
        return reverse_lazy("home:edit-profile")


class DashboardView(LoginRequiredMixin, View):
    template_name = "home/dashboard.html"

    def get(self, request, *args, **kwargs):
        context = {"form": ProfileUpdateForm(instance=request.user)}
        return render(request, self.template_name, context)


class BecomeATutorView(LoginRequiredMixin, TemplateView):
    template_name = "home/become-a-tutor.html"

    def get(self, request, *args, **kwargs):
        form = TutorRequestForm()

        WHATSAPP_GROUP_LINK = get_env_variable("WHATSAPP_GROUP_LINK", "-")

        context = {"form": form}

        if len(WHATSAPP_GROUP_LINK) > 1:
            context["WHATSAPP_GROUP_LINK"] = WHATSAPP_GROUP_LINK

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = TutorRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Request has been sent to Soft Skill Space, "
                + "Kindly book your interview if not already done so. "
                + "See link below",
            )

            return redirect("home:become-a-tutor")
        context = {"form": form}
        return render(request, self.template_name, context)


class AboutUsView(TemplateView):
    template_name = "home/about-us.html"


class ContactUsView(TemplateView):
    template_name = "home/contact-us.html"

    def post(self, request, *args, **Kwargs):
        data = request.POST.dict()
        name = data.get("name")
        email = data.get("email", "")
        subject = data.get("subject")
        message = data.get("message")
        honey_pot = data.get("last_name", "")

        # If the last_name part of the form is filled, then it's most likely a bot
        texts = f"{subject} {email} {message}".lower()
        is_promotion = "http" in texts
        redirect_url = "https://www.google.com"
        url_regex = (
            r'(https?:\/\/(?:www\.|(?!www))'
            + '[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|'
            + 'www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}'
            + '|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}'
            + '|www\.[a-zA-Z0-9]+\.[^\s]{2,})'
        )

        url = re.findall(url_regex, texts)
        if url:
            redirect_url = url[0]

        if is_promotion or len(honey_pot) > 0:
            return redirect(redirect_url)

        send_mail(
            subject=f'{name} sent an email with subject "{subject}"',
            message=message,
            fail_silently=True,
            from_email=email,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
        )

        success_msg = (
            "Your message has been sent. "
            + "SoftSkillSpace Will get back to you as soon as possible 🥂."
        )

        messages.success(request, success_msg)
        return redirect("home:contact-us")


class TermsOfUseView(TemplateView):
    template_name = 'home/terms-of-use.html'
