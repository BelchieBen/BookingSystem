from django.urls import path
from .views import BookingList, BookingView, RoomDetailView, CancelBookingView
from . import views

urlpatterns = [
    path('', views.RoomListView, name='rooms'),
    path('booking/', BookingList.as_view(), name='booking'),
    path('room/<catagory>', RoomDetailView.as_view(), name='RoomDetailView'),
    path('booking/cancel/<pk>',CancelBookingView.as_view(), name='CancelBookingView')
]