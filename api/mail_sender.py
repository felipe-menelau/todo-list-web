from api.tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage

def send_confirmation_email(user):
        mail_subject = 'Activate your account.'
        message = render_to_string('acc_active_email.html', {
                'user': user,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
        email = EmailMessage(
                        mail_subject, message, to=[user.email]
            )
        email.send()
        return

def send_forgot_password_email(user):
        mail_subject = 'Did you forget your password?'
        message = render_to_string('pass_forgot_email.html', {
                'user': user,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
        email = EmailMessage(
                        mail_subject, message, to=[user.email]
            )
        email.send()
        return
