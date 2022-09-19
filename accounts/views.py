from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse

from Cinema import settings
from accounts.forms import PaymentForm, ProfileEditForm, EditUserForm, UserCreat, ProfileForm
from accounts.models import Profile, Payment


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            context = {
                'username': username,
                'error': 'کاربری با این مشخصات یافت نشد'
            }
        else:
            login(request, user)
            if request.GET.get('next'):
                return HttpResponseRedirect(request.GET.get('next'))
            return HttpResponseRedirect(reverse('Ticketing:showtime_list'))
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('Ticketing:showtime_list'))
        context = {}
    return render(request, 'Accounts/login.html', context)
######################################


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('accounts:login'))
######################################


@login_required
def profile_view(request):
    my_profile = Profile.objects.get(user=request.user)
    context = {
        'profile': my_profile
    }
    return render(request, "Accounts/profile.html", context)

######################################


@login_required
def payment_view(request):
    payment = Payment.objects.filter(profile=request.user.profile).order_by('-payment_time')
    payment_c = list(range(1, payment.count() + 1))
    context = {
        'payment': payment,
        'payment_c': payment_c
    }
    return render(request, 'Accounts/payment_show.html', context)
######################################


@login_required
def payment_creat_view(request):
    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            payment_form = payment_form.save(commit=False)
            payment_form.profile = request.user.profile
            payment_form.save()
            request.user.profile.deposit(payment_form.amount)
            return HttpResponseRedirect(reverse('accounts:payment'))
    else:
        payment_form = PaymentForm()
        pass
    context = {
        'payment_form': payment_form
    }
    return render(request, 'Accounts/payment_creat.html', context)

######################################


@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)
        form_user = EditUserForm(request.POST, instance=request.user)
        if profile_form.is_valid() and form_user.is_valid():
            profile_form.save()
            form_user.save()
            return HttpResponseRedirect(reverse('accounts:profile'))
    else:
        profile_form = ProfileEditForm(instance=request.user.profile)
        form_user = EditUserForm(instance=request.user)
        pass
    context = {
        'profile_form': profile_form,
        'form_user': form_user
    }
    return render(request, 'Accounts/profile_edit.html', context)
######################################


def signup(request):
    if request.method == 'POST':
        register = UserCreat(request.POST)
        prof_form = ProfileForm(request.POST)
        if register.is_valid():
            register.save()
            user = User.objects.get(username=register.cleaned_data['username'])
            user.is_staff = False
            if prof_form.is_valid():
                profile = Profile.objects.create(user=user, Birth_date=prof_form.cleaned_data['birth_date'], gender=prof_form.cleaned_data['gender'], mobile=prof_form.cleaned_data['mobile'])
                profile.save()
                user.email = prof_form.cleaned_data['email']
                user.save()
                login(request, user)
                return HttpResponseRedirect(reverse('accounts:profile_edit'))
        pass
    else:
        signup = UserCreat()
        prof_form = ProfileForm()
    context = {
        'signup': signup,
        'prof_form': prof_form
    }
    return render(request, 'Accounts/signup.html', context)
######################################
