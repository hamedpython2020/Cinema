from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Profile(models.Model):
    class Meta:
        verbose_name = 'پروفایل'
        verbose_name_plural = 'پروفایل'
        pass
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='نام کاربری')

    mobile = models.CharField('تلفن همراه', max_length=11, )

    Male = 1
    Female = 2
    Gender_Choices = ((Male, 'مرد'), (Female, 'زن'))
    gender = models.IntegerField('جنسیت', choices=Gender_Choices, null=False, blank=True)
    Birth_date = models.DateField('تاریخ تولد', null=False, blank=True)
    address = models.TextField('آدرس', null=True, blank=True)
    profile_image = models.ImageField('عکس پروفایل', upload_to='users/profile_image/', null=True, blank=True)

    balance = models.IntegerField('موجودی حساب', default=0)

    def __str__(self):
        return self.user.get_full_name()

    def gets_balance(self):
        return 'تومان {}'.format(self.balance)

    def deposit(self, amount):
        self.balance += amount
        self.save()
        pass

    def spend(self, amount):
        if amount > self.balance:
            return False
        else:
            self.balance -= amount
            self.save()
            return True
        pass

###########################################################


class Payment(models.Model):

    class Meta:
        verbose_name = 'پرداخت'
        verbose_name_plural = 'پرداخت'
        pass

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='کاربر')
    amount = models.PositiveIntegerField('مبلغ')
    payment_time = models.DateTimeField('زمان پرداخت', auto_now_add=True)
    payment_cod = models.CharField('رسید پرداخت', max_length=25)

    def __str__(self):
        return 'مبلغ {} تومان برای حساب {}'.format(self.amount, self.profile)
