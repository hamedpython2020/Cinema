from django.urls import path

from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('profile/detail', views.profile_view, name='profile'),
    path('paymetn/list', views.payment_view, name='payment'),
    path('paymetn/creat/', views.payment_creat_view, name='payment_creat'),
    path('profile/edit', views.profile_edit_view, name='profile_edit'),
    # path('profile/change/password', views.change_password, name='password_change')
    path('signup/', views.signup, name='signup'),
    # path('profile/creat', views.profile_creat, name='profile_creat')
    # path('activate/<uidb64>/<token>', views.activate, name='activate'),

]
