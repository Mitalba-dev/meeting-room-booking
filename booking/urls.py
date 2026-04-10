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
    path('', views.dashboard, name='dashboard'),   # 👈 keep this
    path('rooms/', views.room_list, name='room_list'),
    path('bookings/', views.booking_list, name='booking_list'),
    path('create/', views.create_booking, name='create_booking'),
    path('delete/<int:pk>/', views.delete_booking, name='delete_booking'),
    path('register/', views.register, name='register'),
]