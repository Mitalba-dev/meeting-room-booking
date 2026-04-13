from django.shortcuts import render,get_object_or_404,redirect
from .models import Room,Booking
from .forms import BookingForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.utils import timezone



# Create your views here.


def room_list(request):
    rooms = Room.objects.all()
    now = timezone.now()

    room_status = []

    for room in rooms:
        is_booked = Booking.objects.filter(
            room=room,
            end_time__gte=now
        ).exists()

        room_status.append({
            'room': room,
            'is_booked': is_booked
        })

    return render(request, 'booking/room_list.html', {
        'room_status': room_status
    })


@login_required
def booking_list(request):
    bookings = Booking.objects.filter(user=request.user).select_related('room')
    now = timezone.now()
    return render(request, 'booking/booking_list.html', {
        'bookings': bookings,
        'now': now
    })


@login_required
def create_booking(request):
    room_id = request.GET.get('room')

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            return redirect('booking_list')
    else:
        form = BookingForm()
        if room_id:
            form.fields['room'].initial = room_id

    return render(request, 'booking/create_booking.html', {'form': form})

@login_required
def delete_booking(request,pk):

    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    booking.delete()
    return redirect('booking_list')


@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)

    today = timezone.now().date()

    if booking.start_time.date() < today:
        messages.error(request, "Cannot cancel past booking")
    else:
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, "Booking cancelled successfully")

    return redirect('booking_list')


def register(request):
    form = UserCreationForm(request.POST or None)

    for field in form.fields.values():
        field.help_text = None

    if request.method == 'POST':
        for field in form.fields.values():
            field.help_text = None

        if form.is_valid():
            user = form.save()
            # messages.success(request, "Account created successfully")
            return redirect('login')
        # else:
        #     messages.error(request, "Something went wrong")

    return render(request, 'registration/register.html', {'form': form})



@login_required
def dashboard(request):
    now = timezone.now()

    upcoming = Booking.objects.filter(
        user=request.user,
        start_time__gte=now
    ).order_by('start_time')

    current = Booking.objects.filter(
        user=request.user,
        start_time__lte=now,
        end_time__gte=now
    )

    recent = Booking.objects.filter(
        user=request.user,
        end_time__lt=now
    ).order_by('-end_time')[:5]

    context = {
        'upcoming': upcoming,
        'current': current,
        'recent': recent
    }

    return render(request, 'booking/dashboard.html', context)