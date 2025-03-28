# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from events.models import RSVP
from django.conf import settings

@receiver(post_save, sender=RSVP)
def send_rsvp_confirmation(sender, instance, created, **kwargs):
    if created:  # Only send email when a new RSVP is created     
        subject = f'RSVP Confirmation for "{instance.event.name}" '
        message = f"""
        Dear ,{instance.user.first_name} {instance.user.last_name},
        
        Thank you for your RSVP to {instance.event.name}!
        
        You have confirmed that you are Attending the event on {instance.event.date.strftime('%B %d, %Y at %I:%M %p')}.
        
        Event details:
        Location: {instance.event.location}
        Description: {instance.event.description}
        
        We look forward to seeing you there!
        
        Best regards,
        The Event Team
        @mdomarsadek
        """
        
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER, 
            [instance.user.email],    
            fail_silently=False,
        )