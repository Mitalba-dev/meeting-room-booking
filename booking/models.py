from django.db import models

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length = 100)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name

class Booking(models.Model):
    room = models.ForeignKey(Room,on_delete=models.CASCADE,)
    title= models.CharField(max_length = 100)
    user_name = models.CharField(max_length = 100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}-{self.room.name}"