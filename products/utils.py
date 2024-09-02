# from .models import student
import time
from django.core.mail import send_mail,EmailMessage
from django.conf import settings

def run_this_function():
    print("function started")
    time.sleep(1)
    print("function executed")

def send_email_to_client():
    subject = "email"
    message = "checking the programme and again"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ["rookiehaseeb2005@gmail.com"]
    
    send_mail(subject, message, from_email, recipient_list)

def send_email_attachment(subject,message,recipient_list,file_path):
    mail = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=recipient_list,
    )
    mail.attach_file(file_path)
    mail.send()