# Celery Modules
from celery import shared_task

# Django Modules
from django.core.mail import send_mail


@shared_task(
    max_retries=3,
    autoretry_for=(Exception,),
    retry_backoff=True,
)
def send_welcome_email(
    user_email: str,
    username: str,
) -> None:
    
    send_mail(
        subject='Welcome!',
        message=f'Hello {username}, thank you for registration'
        from_email='noreply@gmail.com',
        recipient_list=[user_email],
    )