from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django import forms
from django.forms import ModelForm
from .models import Car


def validate_license_number(license_number):
    if len(license_number) != 8:
        raise ValidationError("License must be exactly 8 characters")
    first_three = license_number[:3]
    if not first_three.isupper() or not first_three.isalpha():
        raise ValidationError(
            "First 3 characters must be uppercase letters"
        )
    if not license_number[3:].isdigit():
        raise ValidationError("Last 5 characters must be digits")
    return license_number


class CarForm(ModelForm):
    class Meta:
        model = Car
        widgets = {
            "drivers": forms.CheckboxSelectMultiple,
        }
        fields = "__all__"


class DriverCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
        )

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])


class DriverLicenseUpdateForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = (
            "license_number",
            "first_name",
            "last_name",
        )

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])
