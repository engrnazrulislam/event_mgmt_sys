from django.db.models.signals import post_save, pre_save, m2m_changed, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from events.models import Event

@receiver(m2m_changed, sender=Event.participants.through)

def notify_on_event_creation(sender, instance, action, **kwargs):
    if action == 'post_add':
        print(instance, instance.participants.all())
        assigned_emails = [emp.email for emp in instance.participants.all()]
        
        print("Checking", assigned_emails)
        send_mail(  
            "New Task Assigned",
            f"You have been assigned for New Task:{instance.title}",
            "tscrpbl@gmail.com",
            assigned_emails,
            fail_silently=False
        )

# POST Delete Signals
@receiver(post_delete, sender=Event)
def delete_associate_details(sender, instance, **kwargs):
    if instance.details:
        print(isinstance)
        instance.details.delete()

        print("Deleted Successfully")