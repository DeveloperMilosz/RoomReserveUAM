from allauth.account.views import ConfirmEmailView as AllauthConfirmEmailView
from allauth.account.views import EmailVerificationSentView as AllauthEmailVerificationSentView
from allauth.account.views import LoginView as AllauthLoginView
from allauth.account.views import LogoutView as AllauthLogoutView
from allauth.account.views import PasswordResetDoneView as AllauthPasswordResetDoneView
from allauth.account.views import PasswordResetFromKeyDoneView as AllauthPasswordResetFromKeyDoneView
from allauth.account.views import PasswordResetFromKeyView as AllauthPasswordResetFromKeyView
from allauth.account.views import PasswordResetView as AllauthPasswordResetView
from allauth.account.views import SignupView as AllauthSignupView
from allauth.account.views import PasswordChangeView as AllauthPasswordChangeView


class LoginView(AllauthLoginView):
    template_name = "pages/auth/login.html"


class LogoutView(AllauthLogoutView): ...


class SignupView(AllauthSignupView):
    template_name = "pages/auth/signup.html"


class EmailVerificationSentView(AllauthEmailVerificationSentView):
    template_name = "pages/auth/email_verification/email_verification_sent.html"


class NewEmailVerificationSentView(AllauthEmailVerificationSentView):
    template_name = "pages/auth/email_verification/new_email_verification_sent.html"


class ConfirmEmailView(AllauthConfirmEmailView):
    template_name = "pages/auth/email_verification/email_confirmation_failed.html"


class PasswordResetView(AllauthPasswordResetView):
    template_name = "pages/auth/reset_password/reset_password.html"

class PasswordChangeView(AllauthPasswordChangeView):
    template_name = "pages/auth/reset_password/password_change.html"


class PasswordResetFromKeyView(AllauthPasswordResetFromKeyView):
    template_name = "pages/auth/reset_password/password_reset_from_key.html"


class PasswordResetDoneView(AllauthPasswordResetDoneView):
    template_name = "pages/auth/reset_password/reset_password_done.html"


class PasswordResetFromKeyDoneView(AllauthPasswordResetFromKeyDoneView):
    template_name = "pages/auth/reset_password/password_reset_from_key_done.html"


login = LoginView.as_view()
logout = LogoutView.as_view()
signup = SignupView.as_view()
email_verification_sent = EmailVerificationSentView.as_view()
new_email_verification_sent = NewEmailVerificationSentView.as_view()
confirm_email = ConfirmEmailView.as_view()
password_reset = PasswordResetView.as_view()
password_reset_from_key = PasswordResetFromKeyView.as_view()
password_reset_done = PasswordResetDoneView.as_view()
password_reset_from_key_done = PasswordResetFromKeyDoneView.as_view()
password_change = PasswordChangeView.as_view()
