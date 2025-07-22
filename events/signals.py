from django.db.models.signals import post_save, pre_save, m2m_changed, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from events.models import Event, Participant
from django.conf import settings

# @receiver(m2m_changed, sender=Participant.participant_to.through)
# def notify_participants_on_assignment(sender, instance, action, **kwargs):
#     if action == 'post_add':
#         assigned_emails = [p.email for p in instance.participant_to.all()] 
#         send_mail(  
#             "New Task Assigned",
#             f"You have been assigned for New Task:{instance.name}",
#             "tscrpbl@gmail.com",
#             assigned_emails,
#             fail_silently=False
#         )
@receiver(m2m_changed, sender=Participant.participant_to.through)
def notify_on_event_creation(sender, instance, action, **kwargs):
    if action == 'post_add':
        for event in instance.participant_to.all():
            emails = [p.email for p in event.participants.all()]
            print("Sending to:", emails)

            send_mail(
                subject="You have been assigned to an event",
                message=f"You have been assigned to the event: {event.name}",
                from_email='tscrpbl@gmail.com',
                recipient_list=emails,
                fail_silently=False
            )


# POST Delete Signals
@receiver(post_delete, sender=Event)
def delete_events(sender, instance, **kwargs):
    if instance.participants:
        instance.participants.clear()
        print("Deleted Successfully")