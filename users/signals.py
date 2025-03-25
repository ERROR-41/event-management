from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
User = get_user_model()


@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    if created:
        token = default_token_generator.make_token(instance)
        activation_url = f'{settings.FRONTEND_URL}/users/activate/{instance.id}/{token}/'

        subject = 'Activate your account'
        message = f'Please click the link below to activate your account:\n\n{activation_url}'
        recipient_list = [instance.email]

        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
            print(f'Activation email sent to {instance.email}')
        except Exception as e:
            # Log the exception
            print(f'Error sending activation email: {e}')

@receiver(post_save, sender=User)
def assign_role(sender, instance, created, **kwargs):
    if created:
        # Check if the user is already in a group to prevent recursion
        if not instance.groups.exists():
            participant_group, created = Group.objects.get_or_create(name='Participant') 
            # Use update to avoid triggering the post_save signal again
            instance.groups.add(participant_group)
            # Remove instance.save() to prevent recursion
