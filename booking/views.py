from django import forms
from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse_lazy
from .models import Room,Booking
from .forms import BookingForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.admin.views.decorators import staff_member_required




# Create your views here.
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        user = self.request.user

        if user.is_staff:
            return reverse_lazy('admin_dashboard')
        else:
            return reverse_lazy('dashboard')
        

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

            messages.success(request, "Booking created successfully!")
            return redirect('booking_list')

        else:
            for field_errors in form.errors.values():
                for error in field_errors:
                    messages.error(request, error)

            return redirect('create_booking')

    else:
        form = BookingForm()
        if room_id:
            form.fields['room'].initial = room_id

    return render(request, 'booking/create_booking.html', {'form': form})


@login_required
def update_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)

    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)

        if form.is_valid():
            form.save()
            messages.success(request, "Booking updated successfully!")
            return redirect('booking_list')

        else:
            for field_errors in form.errors.values():
                for error in field_errors:
                    messages.error(request, error)

            return redirect('update_booking', pk=pk)

    else:
        form = BookingForm(instance=booking)

    return render(request, 'booking/update_booking.html', {
        'form': form
    })


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
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect('login')

        else:
            for field_errors in form.errors.values():
                for error in field_errors:
                    messages.error(request, error)

            return redirect('register')

    return render(request, 'registration/register.html', {'form': form})



@login_required
def dashboard(request):

    if request.user.is_staff:
        return redirect('admin_dashboard')
    
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


def is_admin(user):
    return user.is_staff


@user_passes_test(is_admin)
def admin_dashboard(request):
    total_users = User.objects.count()
    total_rooms = Room.objects.count()
    total_bookings = Booking.objects.count()
    active_bookings = Booking.objects.filter(status='active').count()

    context = {
        'total_users': total_users,
        'total_rooms': total_rooms,
        'total_bookings': total_bookings,
        'active_bookings': active_bookings,
    }

    return render(request, 'admin_dashboard.html', context)


@user_passes_test(is_admin)
def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})


# @user_passes_test(is_admin)
# def room_manage(request):
#     rooms = Room.objects.all()
#     return render(request, 'booking/room_manage.html', {'rooms': rooms})


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'capacity']


@user_passes_test(is_admin)
def room_manage(request):
    rooms = Room.objects.all()
    return render(request, 'booking/admin/room_list.html', {'rooms': rooms})


@user_passes_test(is_admin)
def room_create(request):
    form = RoomForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('room_manage')

    return render(request, 'booking/admin/room_form.html', {'form': form})


@user_passes_test(is_admin) 
def room_update(request, pk):
    room = get_object_or_404(Room, pk=pk)
    form = RoomForm(request.POST or None, instance=room)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('room_manage')

    return render(request, 'booking/admin/room_form.html', {'form': form})


@user_passes_test(is_admin)
def room_delete(request, pk):
    room = get_object_or_404(Room, pk=pk)
    room.delete()
    return redirect('room_manage')


@staff_member_required
def admin_booking_list(request):
    bookings = Booking.objects.select_related('room', 'user').order_by('-start_time')
    
    return render(request, 'booking/admin/booking_list.html', {
        'bookings': bookings
    })