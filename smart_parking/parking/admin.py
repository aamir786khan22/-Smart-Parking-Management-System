from django.contrib import admin
from .models import  ParkingSlot    #, Booking,Profile

# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'phone', 'vehicle_no')

@admin.register(ParkingSlot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ('slot_number', 'status', 'last_updated')
    list_filter = ('status',)

# @admin.register(Booking)
# class BookingAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'slot', 'vehicle_no', 'status', 'time_in', 'time_out')
#     list_filter = ('status',)
