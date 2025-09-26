from django.core.management.base import BaseCommand
from parking.models import ParkingSlot

class Command(BaseCommand):
    help = "Create sample parking slots S1..S12 if not exist"

    def handle(self, *args, **kwargs):
        created = 0
        for i in range(1, 13):
            num = f"S{i}"
            obj, was_created = ParkingSlot.objects.get_or_create(slot_number=num)
            if was_created:
                created += 1
        self.stdout.write(self.style.SUCCESS(f"Done. Slots created: {created}"))
