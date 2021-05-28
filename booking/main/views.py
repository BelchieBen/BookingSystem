from django import http
from django.views.generic.edit import DeleteView
from .forms import availabilityForm
from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, FormView, View, DeleteView
from .models import Booking, Room
from .forms import availabilityForm
from main.booking_functions.availability import check_availability
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

@login_required
def RoomListView(request):
    room = Room.objects.all()[0]
    room_catagories = dict(room.Room_Catagories)
    room_values = room_catagories.values()
    room_list = []
    for room_catagory in room_catagories:
        room = room_catagories.get(room_catagory)
        room_url = reverse('RoomDetailView', kwargs={'catagory':room_catagory})
        room_list.append((room, room_url))

    context = {
        'room_list':room_list,
    }
    return render(request, "main/roomss.html", context ) 

class BookingList(LoginRequiredMixin, ListView):
    model = Booking
    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            booking_list = Booking.objects.all()
            return booking_list
        else:
            booking_list = Booking.objects.filter(user=self.request.user)
            return booking_list

class RoomDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        catagory = self.kwargs.get('catagory', None)
        form = availabilityForm()
        room_list = Room.objects.filter(catagory = catagory)
        
        if len(room_list)>0:
            room = room_list[0]
            room_catagory = dict(room.Room_Catagories).get(room.catagory, None)
            context = {
                'room_catagory' : room_catagory,
                'form' : form
            }
            return render(request, 'main/room_detail.html', context)
        else:
            return HttpResponse('Catagory does not exist')
    def post(self, request, *args, **kwargs):
        catagory = self.kwargs.get('catagory', None)
        room_list = Room.objects.filter(catagory = catagory)
        form = availabilityForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

        available_rooms=[]
        for room in room_list:
            if check_availability(room, data['check_in'], data['check_out']):
                available_rooms.append(room)
            
        if len(available_rooms)>0:
            room = available_rooms[0]
            booking = Booking.objects.create(
                user = self.request.user,
                room = room,
                check_in = data['check_in'],
                check_out = data['check_out']
            )
            booking.save()
            return HttpResponse(booking)
        else:
            return HttpResponse('All the rooms in this catagory are fully booked!')

class CancelBookingView(LoginRequiredMixin, DeleteView):
    model = Booking
    success_url = reverse_lazy('booking')

    
class BookingView(LoginRequiredMixin, FormView):
    form_class = availabilityForm
    template_name = "main/availabilityForm.html"

    def form_valid(self, form):
        data = form.cleaned_data
        room_list = Room.objects.filter(catagory=data['room_catagory'])
        available_rooms=[]
        for room in room_list:
            if check_availability(room, data['check_in'], data['check_out']):
                available_rooms.append(room)
            
        if len(available_rooms)>0:
            room = available_rooms[0]
            booking = Booking.objects.create(
                user = self.request.user,
                room = room,
                check_in = data['check_in'],
                check_out = data['check_out']
            )
            booking.save()
            return HttpResponse(booking)
        else:
            return HttpResponse('All the rooms in this catagory are fully booked!')
