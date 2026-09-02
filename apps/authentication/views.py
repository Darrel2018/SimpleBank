from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .forms import LoginForm
from .services import create_customer
from .services import authenticate_customer


def login_page(request):

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            try:
                user = authenticate_customer(
                    form.cleaned_data["email"],
                    form.cleaned_data["password"],
                )

                request.session["pending_user_id"] = str(user["_id"])

                return redirect("verify")

            except ValueError as error:
                form.add_error(None, str(error))

    else:
        form = LoginForm()

    return render(
        request,
        "authentication/login.html",
        {"form": form},
    )


def register_page(request):

    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            try:
                create_customer(form.cleaned_data)

                return redirect("verify")

            except ValueError as error:
                form.add_error("email", str(error))

    else:
        form = RegistrationForm()

    return render(
        request,
        "authentication/register.html",
        {"form": form},
    )


def verify_page(request):
    return render(request, "authentication/verify.html")


def forgot_password_page(request):
    return render(request, "authentication/forgot_password.html")


def change_password_page(request):
    return render(request, "authentication/change_password.html")


def security_settings_page(request):
    return render(request, "authentication/security_settings.html")


def logout_user(request):
    return render(request, "authentication/login.html")