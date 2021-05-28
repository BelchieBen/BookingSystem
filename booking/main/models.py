from django.db import models
from django.conf import settings
from django.db.models.fields.related import ForeignKey
from django.urls import reverse_lazy

class Room(models.Model):
    Room_Catagories=(
        ('YAC', 'AC'),
        ('NAC', 'NON-AC'),
        ('DEL', 'DELUXE'),
        ('KIN', 'KING'),
        ('QUE', 'QUEEN'),
    )
    number = models.IntegerField()
    catagory = models.CharField(max_length=3, choices=Room_Catagories)
    beds = models.IntegerField()
    capasity = models.IntegerField()

    def __str__(self):
        return f'{self.number}, {self.catagory} with {self.beds} beds for {self.capasity} people'

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()

    def __str__(self):
        return f'{self.user} has booked {self.room} from {self.check_in} to {self.check_out}'

    def get_room_catagory(self):
        room_catagories = dict(self.room.Room_Catagories)
        room_catagory = room_catagories.get(self.room.catagory)
        return room_catagory

    def get_cancel_booking_url(self):
        return reverse_lazy('CancelBookingView', args=[self.pk])


