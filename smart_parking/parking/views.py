from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
import random
from django.core.mail import send_mail
from django.conf import settings

from .forms import SignUpForm, ProfileForm
from .models import ParkingSlot, Profile, Booking

# ---- HOME & AUTH ----
def home(request):
    slots = ParkingSlot.objects.order_by('slot_number')[:6]  # show few
    return render(request, 'home.html', {'slots': slots})

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Signup successful. Please log in.")
            return redirect('login')
        messages.error(request, "Please fix the errors below.")
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect('home')
        messages.error(request, "Invalid credentials.")
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.info(request, "Logged out.")
    return redirect('home')

# ---- SLOTS & BOOKING ----
@login_required
def slots_view(request):
    slots = ParkingSlot.objects.order_by('slot_number')
    my_active = Booking.objects.filter(user=request.user, status='active').first()
    return render(request, 'slots.html', {'slots': slots, 'my_active': my_active})


@login_required
def release_slot(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user, status='active')
    booking.status = 'completed'
    booking.time_out = timezone.now()
    booking.save()

    slot = booking.slot
    slot.status = 'available'
    slot.save()
    messages.success(request, f"Slot {slot.slot_number} released.")
    return redirect('slots')

# ---- PROFILE & HISTORY ----
@login_required
def history_view(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-time_in')
    return render(request, 'history.html', {'bookings': bookings})

@login_required
def account_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile.phone = form.cleaned_data.get('phone', '')
            profile.vehicle_no = form.cleaned_data.get('vehicle_no', '')
            profile.save()
            messages.success(request, "Profile updated.")
            return redirect('account')
        messages.error(request, "Please correct the errors.")
    else:
        form = ProfileForm(initial={'phone': profile.phone, 'vehicle_no': profile.vehicle_no})
    return render(request, 'account.html', {'form': form})

# ---- PARKING SLOT ANALYSIS ----
from Source_Code.detect_parking import analyze_parking

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required
def update_parking_slots(request):
    """
    Updates DB ParkingSlot statuses from analyze_parking()
    and returns a JSON payload for the front-end:
    {
      "updated": <int>,
      "available": <int>,
      "total": <int>,
      "slots": [{"slot_number": "S1", "status": "available", "id": 1}, ...]
    }
    """
    results = analyze_parking()  # [{'slot_number': 'S1', 'status': 'available', ...}, ...]
    slots_payload = []
    available = 0

    for r in results:
      slot, _ = ParkingSlot.objects.get_or_create(slot_number=r["slot_number"])
      slot.status = r["status"]
      slot.save(update_fields=["status", "last_updated"])
      if slot.status == "available":
          available += 1
      slots_payload.append({
          "slot_number": slot.slot_number,
          "status": slot.status,
          "id": slot.id,
      })

    return JsonResponse({
        "updated": len(results),
        "available": available,
        "total": len(results),
        "slots": slots_payload
    })


@login_required
def check_parking(request):
    """
    Returns current slot status as JSON
    """
    result = analyze_parking()
    return JsonResponse(result)


def send_verification_email(user_email, slot_id):
    """
    Generates a 6-digit verification code, sends it via email,
    and returns the code.
    """
    code = str(random.randint(100000, 999999))  # 6-digit code

    subject = f"Parking Slot Verification Code for Slot {slot_id}"
    message = f"Dear user,\n\nYour verification code for booking Slot {slot_id} is: {code}\n\nPlease enter this code to confirm your booking.\n\nThank you!"
    from_email = settings.DEFAULT_FROM_EMAIL  # make sure this is set in settings.py
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    
    return code

@login_required
def enter_verification_code(request, slot_id):
    """
    View to enter verification code for a pending booking
    """
    slot = get_object_or_404(ParkingSlot, id=slot_id)
    booking_id = request.session.get('pending_booking_id')

    if not booking_id:
        messages.error(request, "No pending booking found.")
        return redirect('slots')

    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        entered_code = request.POST.get('verification_code', '').strip()
        if entered_code == booking.verification_code:
            booking.verified = True
            booking.save()
            slot.status = 'occupied'
            slot.save()
            del request.session['pending_booking_id']
            messages.success(request, f"Slot {slot.slot_number} booked successfully!")
            return redirect('slots')
        else:
            messages.error(request, "Incorrect verification code!")
            return redirect('enter_verification_code', slot_id=slot_id)

    return render(request, 'enter_verification_code.html', {'slot': slot})

@login_required
def book_slot(request, slot_id):
    slot = get_object_or_404(ParkingSlot, id=slot_id)

    if request.method == 'POST':
        # check if a pending booking exists already
        booking_id = request.session.get('pending_booking_id')
        if booking_id:
            return redirect('enter_verification_code', slot_id=slot_id)

        # get vehicle number
        profile = Profile.objects.filter(user=request.user).first()
        vehicle_no = profile.vehicle_no if profile and profile.vehicle_no else request.POST.get('vehicle_no', '').strip()
        if not vehicle_no:
            messages.error(request, "Please set your vehicle number in Account first.")
            return redirect('account')

        # Create booking & send verification email
        code = send_verification_email(request.user.email, slot.id)
        booking = Booking.objects.create(
            user=request.user,
            slot=slot,
            vehicle_no=vehicle_no,
            verification_code=code,
            verified=False
        )
        request.session['pending_booking_id'] = booking.id
        messages.info(request, f"Verification code sent to {request.user.email}. Please enter the code to confirm booking.")
        return redirect('enter_verification_code', slot_id=slot.id)