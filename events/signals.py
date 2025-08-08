from django.db.models.signals import m2m_changed, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from events.models import Event
from django.conf import settings
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()


@receiver(m2m_changed, sender=Event.participant.through)
def notify_employees_on_task_creation(sender, instance, action, **kwargs):
    if action == 'post_add':
        assigned_emails = [user.email for user in instance.participant.all() if user.email]
        send_mail(  
            "New Task Assigned",
            f"You have been assigned for New Task:{instance.name}",
            "tscrpbl@gmail.com",
            assigned_emails,
            fail_silently=False
        )

@receiver(post_delete, sender=Event)
def delete_events(sender, instance, **kwargs):
    if instance.participant.exists():
        instance.participant.clear()
        print("Deleted Event and cleared all participants.")
