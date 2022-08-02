from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm

from home.models import CustomUser, MailingList
from softskillspace.utils.forms import CssForm


class ProfileUpdateForm(UserChangeForm, CssForm):
    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "about",
            "email",
            "mobile_no",
            "gender",
            "country",
            "date_of_birth",
            # "profile_pic",
        ]

        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last name"}),
            "about": forms.Textarea(attrs={"placeholder": "About me", "rows": 6}),
            "email": forms.EmailInput(
                attrs={"placeholder": "Email address", "readonly": True}
            ),
            "mobile_no": forms.TextInput(
                attrs={"type": "tel", "placeholder": "077 1234 5678"}
            ),
            "date_of_birth": forms.DateInput(
                attrs={
                    "type": "date",
                    "placeholder": "Date of birth",
                    "max": "2012-01-01",
                },
                format="%Y-%m-%d",
            ),
            # "profile_pic": forms.FileInput(),
        }


class PasswordUpdateForm(PasswordChangeForm, CssForm):
    class Meta:
        model = CustomUser
        fields = "__all__"


class MailingListForm(forms.ModelForm, CssForm):
    class Meta:
        model = MailingList
        exclude = ["visible", "categories"]

        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "class": "border-0 me-1",
                    "placeholder": "Enter your email"})}
