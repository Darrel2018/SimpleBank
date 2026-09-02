from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .forms import LoginForm, OTPForm
from .services import create_customer
from .services import authenticate_customer
from .services import verify_demo_otp
from .services import complete_customer_login
from .utils import generate_otp, otp_expiry_time


def login_page(request):

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            try:
                user = authenticate_customer(
                    form.cleaned_data["email"],
                    form.cleaned_data["password"],
                )

                otp = generate_otp()

                request.session["pending_user_id"] = str(user["_id"])
                request.session["otp_code"] = otp
                request.session["otp_expires"] = otp_expiry_time().isoformat()

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

    if not request.session.get("pending_user_id"):
        return redirect("login")

    if request.method == "POST":

        form = OTPForm(request.POST)

        if form.is_valid():

            try:
                verify_demo_otp(
                    request.session,
                    form.cleaned_data["otp"],
                )

                complete_customer_login(request.session)

                return redirect("dashboard")

            except ValueError as error:
                form.add_error(None, str(error))

    else:
        form = OTPForm()

    context = {
        "form": form,
        "demo_otp": request.session.get("otp_code"),
    }

    return render(
        request,
        "authentication/verify.html",
        context,
    )

def forgot_password_page(request):
    return render(request, "authentication/forgot_password.html")


def change_password_page(request):
    return render(request, "authentication/change_password.html")


def security_settings_page(request):
    return render(request, "authentication/security_settings.html")


def logout_user(request):
    return render(request, "authentication/login.html")