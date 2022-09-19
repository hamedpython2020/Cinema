from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.urls import reverse

from Ticketing.forms import Showtime_form
from Ticketing.models import Movie, Cinema, ShowTime, Ticket


#####################################################################################

def cinema_list(request):
    cinemas = Cinema.objects.all()
    cinemas_c = Cinema.objects.all().count()
    context = {
        'cinemas': cinemas,
        'cinemas_c': cinemas_c
    }
    return render(request, 'ticketing/cinema_list.html', context)
#####################################################################################


def movie_list(request):
    movies = Movie.objects.all()
    movies_c = Movie.objects.all().count()
    context = {
        'movies': movies,
        'movies_c': movies_c
    }
    return render(request, 'ticketing/movie_list.html', context)
#####################################################################################


def cinema_detail(request, cinema_id):
    cinemas = get_object_or_404(Cinema, pk=cinema_id)
    context = {
        'cinemas': cinemas
    }
    return render(request, 'ticketing/cinema_detail.html', context)
#####################################################################################


def movie_detail(request, movie_id):
    movies = get_object_or_404(Movie, pk=movie_id)
    context = {
        'movies': movies,
    }
    return render(request, 'ticketing/movie_detail.html', context)
#####################################################################################


@login_required
def showtime_list(request):
    search_box = Showtime_form(request.GET)
    showtime = ShowTime.objects.all()
    if search_box.is_valid():
        showtime = showtime.filter(movie__name__contains=search_box.cleaned_data['movie_name'])
        if search_box.cleaned_data['sale_access']:
            showtime = showtime.filter(status=ShowTime.sale_started)
        if search_box.cleaned_data['movie_length_min']:
            showtime = showtime.filter(movie__length__gte=search_box.cleaned_data['movie_length_min'])
        if search_box.cleaned_data['movie_length_max']:
            showtime = showtime.filter(movie__length__lte=search_box.cleaned_data['movie_length_max'])
        if search_box.cleaned_data['cinema']:
            showtime = showtime.filter(cinema=search_box.cleaned_data['cinema'])
        min_price, max_price = search_box.get_price()
        if min_price is not None:
            showtime = showtime.filter(price__gte=min_price)
        if max_price is not None:
            showtime = showtime.filter(price__lte=max_price)
        pass

    showtime = showtime.order_by('start_time')
    showtime_c = showtime.count()
    context = {
        'search_box': search_box,
        'showtime': showtime,
        'showtime_c': showtime_c
    }
    return render(request, 'ticketing/showtime_list.html', context)

#####################################################################################


@login_required
def showtime_detail(request, showtime_id):
    showtime = get_object_or_404(ShowTime, pk=showtime_id)
    context = {
        'showtime': showtime,
    }
    if request.method == 'POST':
        try:
            ticket_count = int(request.POST['ticket_count'])
            assert showtime.status == ShowTime.sale_started, 'امکان خرید بلیط وجود ندارد'
            assert showtime.salable_seat >= ticket_count, ' تعداد صندلی بیش از ظرفیت باقی مانده می باشد '
            total_price = ticket_count * int(showtime.price)
            assert request.user.profile.spend(total_price), 'موجودی کافی نمی باشد'
            ticket = Ticket.objects.create(showtime=showtime, buyer=request.user.profile, seat_number=ticket_count)
            showtime.seat_counter(ticket_count)
        except Exception as e:
            context['error'] = str(e)
            pass
        else:
            return HttpResponseRedirect(reverse('Ticketing:ticket_detail', kwargs={'ticket_id': ticket.id}))
    return render(request, 'ticketing/showtime_detail.html', context)

#####################################################################################


@login_required
def ticket_list(request):
    tickets = Ticket.objects.filter(buyer=request.user.profile).order_by('-buy_time')
    tickets_c = Ticket.objects.filter(buyer=request.user.profile).count()
    context = {
        'tickets': tickets,
        'tickets_c': tickets_c
    }
    return render(request, 'ticketing/ticket_list.html', context)
#####################################################################################


def ticket_detail(request, ticket_id):
    tickets = get_object_or_404(Ticket, pk=ticket_id)
    # acc_ticket = Ticket.objects.get().ordering(Ticket.showtime.s)
    context = {
        'tickets': tickets,
        # 'tickets_c': tickets_c
    }
    return render(request, 'ticketing/ticket_detail.html', context)
