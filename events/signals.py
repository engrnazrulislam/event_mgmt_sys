from django.db.models.signals import m2m_changed, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from events.models import Event
from django.conf import settings
from django.contrib.auth.models import User

@receiver(m2m_changed, sender=Event.participant.through)
def notify_on_event_rsvp(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        for user_id in pk_set:
            try:
                user = User.objects.get(pk=user_id)
                send_mail(
                    subject="RSVP Confirmation",
                    message=f"Dear {user.get_full_name() or user.username},\n\nYou have been added as a participant to the event: '{instance.name}' scheduled on {instance.date}.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False
                )
                print(f"Email sent to {user.email}")
            except User.DoesNotExist:
                print(f"User with ID {user_id} not found.")

@receiver(post_delete, sender=Event)
def delete_events(sender, instance, **kwargs):
    if instance.participant.exists():
        instance.participant.clear()
        print("Deleted Event and cleared all participants.")
