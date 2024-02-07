from django.core.mail import EmailMessage
import os

class Util:
    @staticmethod
    def send_mail(data):
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],
            from_email=os.environ.get('EMAIL_HOST_USER'),  # Replace with your actual email address
            to=[data['to_email']],  # Use square brackets for a list of email addresses
        )
        email.send()
