from django import forms
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from accounts.models import Payment, Profile


###################################


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'payment_cod']
        pass

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount % 1000 != 0:
            raise ValidationError("مقدار وارد شده باید ضریبی از 1000 تومان باشد")
        if amount < 5000:
            raise ValidationError('مقدار وارد شده باید بیشتر از 5000 تومان باشد')
        return amount

    def clean_payment_cod(self):
        code = self.cleaned_data['payment_cod']
        try:
            assert code.startswith('bank-')
            assert code.endswith('#')
            part = code.split('-')
            assert len(part) == 3
            int(part[1])
            pass
        except:
            raise ValidationError('رسید پرداخت قالب درستی ندارد')
        return code

    def clean(self):
        super().clean()
        amount = self.cleaned_data.get('amount')
        code = self.cleaned_data.get('payment_cod')
        if amount is not None and code is not None:
            try:
                assert int(code.split('-')[1]) == amount
            except:
                raise ValidationError('رسید با مبلغ مطابقت ندارد')

###################################


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['mobile', 'gender', 'address', 'profile_image']
        pass

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        try:
            assert mobile.startswith('09') or mobile.startswith('+98'), 'شماره تلفن باید با 09 یا 98+ شروع شود'
            assert int(mobile), 'موبایل را درست وارد کنید'
        except:
            raise ValidationError('موبایل قالب درستی ندارد')
        return mobile
    pass

#####################################


class EditUserForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'email']
    password = None

#####################################


class UserCreat(UserCreationForm):
    # first_name = forms.CharField(label='نام', required=False, max_length=20)
    # last_name = forms.CharField(label='نام خانوادگی', required=False, max_length=30)
    pass

#####################################


class ProfileForm(forms.Form):

    l = []
    for i in range(1979, 2040):
        l.append(str(i))
        pass

    mobile = forms.CharField(label='تلفن همراه', max_length=11, required=False)
    birth_date = forms.DateField(label='تاریخ تولد', widget=forms.SelectDateWidget(years=l))
    Male = 1
    Female = 2
    Gender_Choices = ((Male, 'مرد'), (Female, 'زن'))
    gender = forms.ChoiceField(label='جنسیت', choices=Gender_Choices)
    address = forms.CharField(label='آدرس', widget=forms.Textarea, required=False)
    email = forms.EmailField(label='ایمیل', required=True)

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        try:
            assert mobile.startswith('09') or mobile.startswith('+98'), 'شماره تلفن باید با 09 یا 98+ شروع شود'
            assert int(mobile), 'موبایل را درست وارد کنید'
        except:
            raise ValidationError('موبایل قالب درستی ندارد')
        return mobile
