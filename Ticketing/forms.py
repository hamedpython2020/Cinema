from django import forms

from Ticketing.models import Cinema


class Showtime_form (forms.Form):
    movie_name = forms.CharField(max_length=100, label='نام فیلم', required=False)
    sale_access = forms.BooleanField(label='سانس های قابل خرید', required=False)
    movie_length_max = forms.IntegerField(label='حداکثر زمان فیلم', max_value=200, min_value=20, required=False)
    movie_length_min = forms.IntegerField(label='حداقل زمان فیلم', min_value=20, max_value=200, required=False)
    any_price = '0'
    under_10 = '1'
    between_10_to_15 = '2'
    between_15_to_20 = '3'
    more_than20 = '4'
    range_of_price = (
        (any_price, 'هر قیمتی'),
        (under_10, 'زیر 10 هزار تومان'),
        (between_10_to_15, 'بین 10 تا 15 هزار تومان'),
        (between_15_to_20, 'بین 15 تا 20 هزار تومان'),
        (more_than20, 'بیشتر از 20 هزار تومان')
    )
    price_range = forms.ChoiceField(label='محدوده قیمت', choices=range_of_price, required=False)

    cinema = forms.ModelChoiceField(label='نام سینما', queryset=Cinema.objects.all(), required=False)

    def get_price(self):
        price_level = self.cleaned_data['price_range']
        if price_level == Showtime_form.under_10:
            return None, 10000
        elif price_level == Showtime_form.between_10_to_15:
            return 10000, 15000
        elif price_level == Showtime_form.between_15_to_20:
            return 15000, 20000
        elif price_level == Showtime_form.more_than20:
            return 20000, None
        else:
            return None, None
    pass
