from django import forms
from django.core.exceptions import ValidationError
import re


class RegistrationForm(forms.Form):
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={"autocomplete": "given-name"})
    )
    
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={"autocomplete": "family-name"})
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"autocomplete": "email"})
    )

    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={"autocomplete": "tel"})
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password"}
        )
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password"}
        )
    )

    accept_terms = forms.BooleanField(required=True)

    def clean_first_name(self):
        first_name = self.cleaned_data["first_name"].strip()

        if len(first_name) < 2:
            raise ValidationError(
                "First name must contain at least 2 characters."
            )

        return first_name.title()

    def clean_last_name(self):
        last_name = self.cleaned_data["last_name"].strip()

        if len(last_name) < 2:
            raise ValidationError(
                "Last name must contain at least 2 characters."
            )

        return last_name.title()

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip().replace(" ", "")

        if phone.startswith("0"):
            phone = "+27" + phone[1:]
        elif phone.startswith("27"):
            phone = "+" + phone
        elif not phone.startswith("+"):
            raise ValidationError("Enter a valid South African phone number.")

        phone_pattern = r"^\+[1-9][0-9]{8,14}$"

        if not re.match(phone_pattern, phone):
            raise ValidationError("Enter a valid phone number.")

        return phone

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password:
            if len(password) < 8:
                raise ValidationError(
                    "Password must contain at least 8 characters."
                )

            if not re.search(r"[A-Z]", password):
                raise ValidationError(
                    "Password must contain an uppercase letter."
                )

            if not re.search(r"[a-z]", password):
                raise ValidationError(
                    "Password must contain a lowercase letter."
                )

            if not re.search(r"[0-9]", password):
                raise ValidationError(
                    "Password must contain a number."
                )

            if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
                raise ValidationError(
                    "Password must contain a special character. For Example: !@#$%^&*"
                )

        if password and confirm_password:
            if password != confirm_password:
                raise ValidationError(
                    "Passwords do not match."
                )

        return cleaned_data