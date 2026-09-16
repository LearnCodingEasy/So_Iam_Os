# users_accounts/forms.py

from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    PasswordChangeForm,
)

from .models import User


class SignupForm(UserCreationForm):

    class Meta:
        model = User

        fields = [
            "name",
            "surname",
            "email",
            "date_of_birth",
            "gender",
            "password1",
            "password2",
        ]

        widgets = {
            "date_of_birth": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),
        }

    def clean_email(self):
        email = self.cleaned_data["email"].lower()

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "This email is already registered."
            )

        return email


class ProfileForm(forms.ModelForm):

    class Meta:
        model = User

        fields = [
            "name",
            "surname",
            "email",
            "date_of_birth",
            "gender",
            "avatar",
            "cover",
            "skills",
            "is_online",
        ]

        widgets = {
            "date_of_birth": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),
        }

    def clean_email(self):
        email = self.cleaned_data["email"].lower()

        queryset = User.objects.filter(
            email=email
        ).exclude(
            pk=self.instance.pk
        )

        if queryset.exists():
            raise forms.ValidationError(
                "This email is already registered."
            )

        return email
