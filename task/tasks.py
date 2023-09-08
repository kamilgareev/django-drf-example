from celery import shared_task
from django.core.mail import EmailMessage, get_connection
from django.conf import settings


@shared_task(bind=True)
def send_otp_email_celery(self, email, otp):
    with get_connection(
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_tls=settings.EMAIL_USE_TLS
    ) as connection:
        subject = 'Login verification'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        message = f'Your verification code is {otp}'
        sent = EmailMessage(subject, message, email_from, recipient_list,
                            connection=connection).send()
    return sent
