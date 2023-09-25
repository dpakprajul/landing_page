# generate_data/management/commands/generate_random_data.py

import random
from django.core.management.base import BaseCommand
from notes.models import Notes  # Import your Notes model

class Command(BaseCommand):
    help = 'Generate and import random data into the database'

    def handle(self, *args, **kwargs):
        for _ in range(100):  # Generate 100 records
            title = f"Title {random.randint(1, 100)}"
            text = f"Random text: {random.randint(1, 1000)}"
            number = random.randint(1, 1000)

            # Insert data into the database using your model
            Notes.objects.create(title=title, text=text, number=number)

        self.stdout.write(self.style.SUCCESS('Successfully generated and imported random data.'))
