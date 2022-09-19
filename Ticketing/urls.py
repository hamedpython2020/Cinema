from django.urls import path

from Ticketing import views

app_name = 'Ticketing'
urlpatterns = [
    path('cinema/list/', views.cinema_list, name='cinema_list'),
    path('movie/detail/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('movie/list/', views.movie_list, name='movie_list'),
    path('cinema/detail/<int:cinema_id>/', views.cinema_detail, name='cinema_detail'),
    path('showtime/list/', views.showtime_list, name='showtime_list'),
    path('showtime/detail/<int:showtime_id>/', views.showtime_detail, name='showtime_detail'),
    path('ticket/list/', views.ticket_list, name='ticket_list'),
    path('ticket/detail/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),

]