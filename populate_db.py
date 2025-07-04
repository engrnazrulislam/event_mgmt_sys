import os
import django
from faker import Faker
import random
from events.models import Event, Participant, Category

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_mgmt_sys.settings')
django.setup()

# Function to populate the database
def populate_db():
    fake = Faker()

    # Create Categories
    categories = [Category.objects.create(
        name=fake.word().capitalize(),
        descriptions=fake.sentence()
    ) for _ in range(5)]
    print(f"Created {len(categories)} categories.")

    # Create Events
    events = []
    for _ in range(10):
        event = Event.objects.create(
            name=fake.catch_phrase(),
            description=fake.text(max_nb_chars=200),
            date=fake.date_between(start_date="+1d", end_date="+30d"),
            location=fake.city(),
            category=random.choice(categories)
        )
        events.append(event)
    print(f"Created {len(events)} events.")

    # Create Participants
    participants = []
    for _ in range(20):
        participant = Participant.objects.create(
            name=fake.name(),
            email=fake.email()
        )
        participant.participant_to.set(random.sample(events, random.randint(1, 4)))
        participants.append(participant)
    print(f"Created {len(participants)} participants.")

    print("Database populated successfully!")

# Run the function
if __name__ == '__main__':
    populate_db()
