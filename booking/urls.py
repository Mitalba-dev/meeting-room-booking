from django.urls import path
from . import views

# urlpatterns = [
#     path('',views.room_list,name='room_list'),
#     path('bookings/',views.booking_list,name='booking_list'),
#     path('create/',views.create_booking,name='create_booking'),
#     path('delete/<int:pk>/',views.delete_booking,name='delete_booking'),
#     path('register/', views.register, name='register'),
# ]
# urlpatterns = [
#     path('', views.room_list, name='room_list'),   # /app/
#     path('bookings/', views.booking_list, name='booking_list'),
#     path('create/', views.create_booking, name='create_booking'),
#     path('delete/<int:pk>/', views.delete_booking, name='delete_booking'),
#     path('register/', views.register, name='register'),
#     path('', views.dashboard, name='dashboard'),
# ]
urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('rooms/', views.room_list, name='room_list'),
    path('bookings/', views.booking_list, name='booking_list'),
    path('create-booking/', views.create_booking, name='create_booking'),
    path('cancel/<int:pk>/', views.cancel_booking, name='cancel_booking'),
    path('booking/<int:pk>/edit/', views.update_booking, name='update_booking'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('users/', views.user_list, name='user_list'),
    path('register/', views.register, name='register'),

    path('manage-rooms/rooms/', views.room_manage, name='room_manage'),
    path('manage-rooms/rooms/create/', views.room_create, name='room_create'),
    path('manage-rooms/rooms/edit/<int:pk>/', views.room_update, name='room_update'),
    path('manage-rooms/rooms/delete/<int:pk>/', views.room_delete, name='room_delete'),
    path('manage-bookings/bookings/', views.admin_booking_list, name='admin_booking_list')
]