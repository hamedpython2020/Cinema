from django.db import models

# Create your models here.
import accounts.models


class Movie(models.Model):
    class Meta:
        verbose_name = 'فیلم'
        verbose_name_plural = 'فیلم'
    name = models.CharField('عنوان', max_length=100)
    director = models.CharField('کارگردان', max_length=100)
    year = models.IntegerField('سال تولید')
    length = models.IntegerField('مدت زمان فیلم')
    description = models.TextField('توضیحات', null=True)
    poster = models.ImageField('پوستر', upload_to='movie_posters/',)

    def __str__(self):
        return self.name
    pass


class Cinema (models.Model):
    class Meta:
        verbose_name = 'سالن سینما'
        verbose_name_plural = 'سالن سینما'
    Cod = models.IntegerField('شماره پروانه', primary_key=True)
    name = models.CharField('نام سالن', max_length=50)
    city = models.CharField('شهر', max_length=30, default='مشهد')
    capacity = models.IntegerField('ظرفیت')
    phone = models.CharField('شماره', max_length=50, null=True)
    address = models.TextField('آدرس', null=True)
    image = models.ImageField('تصویر', upload_to='cinema_images/', blank=True)

    def __str__(self):
        return self.name
    pass


class ShowTime (models.Model):
    class Meta:
        verbose_name = 'سانس'
        verbose_name_plural = 'سانس'

    movie = models.ForeignKey('Movie', on_delete=models.PROTECT, verbose_name='نام فیلم')
    cinema = models.ForeignKey('Cinema', on_delete=models.PROTECT, verbose_name='سالن سینما')

    start_time = models.DateTimeField('زمان اغاز')
    price = models.IntegerField('قیمت')
    salable_seat = models.IntegerField('صندلی های قابل فروش')
    soled_seat = models.IntegerField('صندلی های فروخته شده')

    sale_not_started = 1
    sale_started = 2
    ticket_finished = 3
    sale_ended = 4
    Movie_played = 5
    show_cancelled = 6
    status_choices = (
        (1, 'فروش شروع نشده'),
        (2, 'فروش اغاز شد'),
        (3, 'بلیط تمام شد'),
        (4, 'فروش به اتمام رسید'),
        (5, 'فیلم پخش شد'),
        (6, 'فیلم کنسل شد')
    )
    status = models.IntegerField('وضعیت فروش', choices=status_choices)

    def free_seats(self):
        free_seats = self.salable_seat-self.soled_seat
        return free_seats

    def __str__(self):
        return 'فیلم {} \n در سی    نما {}  \n در تایمه  {}'.format(self.movie, self.cinema, self.start_time)

    def get_price_display(self):
        return " {} تومان ".format(self.price)

    def seat_counter(self, amount):
        try:
            assert isinstance(amount, int) and amount > 0, 'مقدار ورودی معتبر نیست'
            assert ShowTime.free_seats(self) >= amount, 'تعداد صندلی بیش از حد ظرفیت است'
            assert self.status == ShowTime.sale_started, 'امکان خرید بلیط این سانس وجود ندارد'
            self.soled_seat += amount
            if self.free_seats() == 0:
                self.status = ShowTime.ticket_finished
                pass
            self.save()
        except Exception as e:
            return e
    pass


class Ticket (models.Model):

    class Meta:
        verbose_name = 'بلیط'
        verbose_name_plural = 'بلیط'
        pass

    showtime = models.ForeignKey(ShowTime, on_delete=models.PROTECT, verbose_name='سانس')
    buyer = models.ForeignKey(accounts.models.Profile, on_delete=models.PROTECT, verbose_name='خریدار')
    seat_number = models.IntegerField('تعداد صندلی', default=0)
    buy_time = models.DateTimeField('زمان  خرید', auto_now_add=True)

    def __str__(self):
        return "{}  بلیط به نام  {}  برای فیلم {}".format(self.seat_number, self.buyer, self.showtime.movie)