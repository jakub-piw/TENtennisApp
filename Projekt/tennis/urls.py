from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns=[
    #path('', include('django.contrib.auth.urls')),
    path('login', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change_done', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name="password_change_done"),
    path('', views.home, name='home'),
    path('courts', views.courts, name="courts"),
    path('trenerzy', views.trenerzy, name="trenerzy"),
    path('profil', views.profile, name='profil'),
    path("register", views.register, name="register"),
    path('booking', views.booking, name='booking'),
    path('thanks', views.thanks, name='thanks'),
    path('discounts', views.discount, name='discounts'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.passwordResetConfirm, name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path("booking/edit/<int:pk>", views.updateBooking, name="update_booking"),
    path("booking/cancel/<int:pk>", views.deleteBooking, name="delete_booking")
]