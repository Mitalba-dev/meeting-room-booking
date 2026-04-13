from django.forms import ModelForm
from .models import Booking
from django.core.exceptions import ValidationError
from datetime import timedelta
from django import forms


class BookingForm(forms.ModelForm):
    class Meta:
        model=Booking
        fields  = ["room","title","start_time","end_time"]
        widgets = {
            "start_time":forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            "end_time":forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

    def clean(self):
        data = super().clean()

        room = data.get('room')
        start_time = data.get("start_time")
        end_time = data.get("end_time")

        if not room or not start_time or not end_time:
            return data
        
        #validation
        if start_time>=end_time:
            raise ValidationError("End time must be greater then start time")

        buffer = timedelta(minutes=10)
        new_start = start_time - buffer
        new_end = end_time + buffer

        db_room = Booking.objects.filter(room=room)
        
        if self.instance.pk:
            db_room = db_room.exclude(pk=self.instance.pk)

        
        for booking in db_room:
            if new_start < booking.end_time and new_end > booking.start_time:
                raise ValidationError(
                    "This room is already booked for the selected time!"
                )
        return data

