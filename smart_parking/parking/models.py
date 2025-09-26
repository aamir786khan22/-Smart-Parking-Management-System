from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    vehicle_no = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"

class ParkingSlot(models.Model):
    STATUS_CHOICES = (('available', 'Available'), ('occupied', 'Occupied'))
    slot_number = models.CharField(max_length=10, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Slot {self.slot_number} - {self.status}"

class Booking(models.Model):
    STATUS_CHOICES = (('active', 'Active'), ('completed', 'Completed'), ('cancelled', 'Cancelled'))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slot = models.ForeignKey(ParkingSlot, on_delete=models.CASCADE)
    vehicle_no = models.CharField(max_length=20)
    time_in = models.DateTimeField(auto_now_add=True)
    time_out = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    verification_code = models.CharField(max_length=6, blank=True, null=True)  # NEW FIELD
    verified = models.BooleanField(default=False)  # NEW FIELD

    def __str__(self):
        return f"Booking #{self.id} - {self.user.username} - {self.slot.slot_number}"
