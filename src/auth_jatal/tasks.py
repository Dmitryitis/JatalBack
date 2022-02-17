import logging
from typing import Iterable

from django.contrib.auth import get_user_model
from django.core import mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags

from NewsPortal import settings
from NewsPortal.celery import app
from NewsPortal.settings import DOMAIN_NAME

User = get_user_model()


@app.task
def email_site(user_id, token, recipient):
    href = DOMAIN_NAME + reverse('password_reset', kwargs={'user_id': user_id, 'token': token})
    send_html_email(
        render_to_string(
            'password_reset_email.html',
            {
                "href": href
            }
        ),
        subject=f"Password reset for {recipient}",
        recipients=recipient
    )


logger = logging.getLogger(__name__)


@app.task(name='users-site', queue='default')
def users_site():
    users = User.objects.all()
    logger.info(f'all users: {len(users)} on sites')
    send_mail("Привет мир!", "Привет", settings.DEFAULT_FROM_EMAIL,
              [settings.DEFAULT_FROM_EMAIL])


def send_html_email(html_message: str, **send_mail_kwargs):
    send_mail(body=strip_tags(html_message), html_message=html_message, **send_mail_kwargs)


def send_mail(subject: str, body: str, recipients: Iterable[str], html_message=None):
    try:
        connection = mail.get_connection()
        mail.send_mail(subject=subject, message=body, from_email=settings.DEFAULT_FROM_EMAIL,
                       recipient_list=[recipients], connection=connection, html_message=html_message)
    except Exception:
        logger.exception("failed to send mail")
