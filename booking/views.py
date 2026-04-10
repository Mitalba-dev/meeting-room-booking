from django.shortcuts import render,get_object_or_404,redirect
from .models import Room,Booking
from .forms import BookingForm

# Create your views here.


def room_list(request):
    room = Room.objects.all()
    return render(request,'booking/room_list.html',{'rooms':room})


def booking_list(request):
    booking = Booking.objects.select_related(
        'room').all().order_by('start_time')
    return render(request,'booking/booking_list.html',{'bookings':booking})


def create_booking(request):
    form = BookingForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save() 
            return redirect('booking_list') 
    return render(
        request,
        'booking/create_booking.html',
        {'form':form}
        )

def delete_booking(request,pk):

    booking = get_object_or_404(Booking,pk=pk)
    booking.delete()
    return redirect('booking_list')
