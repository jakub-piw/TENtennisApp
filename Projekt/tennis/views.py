from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .models import Court, Trener, Booking, Discounts
from .forms import NewUserForm, BookingForm, EditBooking, DeleteBookingForm
from django.contrib.auth import login, get_user_model
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.auth.forms import SetPasswordForm, PasswordResetForm
from .tokens import account_activation_token, password_reset_token


def home(request):
    return render(request, 'tennis/home.html')


def courts(request):
    courts = Court.objects.all()
    context = {'list_of_courts': courts}
    return render(request, 'tennis/courts.html', context=context)


def trenerzy(request):
    coaches = Trener.objects.all()
    context = {'list_of_coaches': coaches}
    return render(request, "tennis/trenerzy.html", context=context)


@login_required
def profile(request):
    reservations = Booking.objects.filter(Q(email=request.user.email))
    context = {'reservations': reservations, 'mail': request.user.email}
    return render(request, "registration/profile.html", context=context)


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = "Activate your blog account."
            message = render_to_string('registration/acc_activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return render(request, template_name='registration/go_to_email.html')
    else:
        form = NewUserForm()
    return render(request=request, template_name="registration/registration.html", context={"register_form": form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return render(request, template_name='registration/after_activation.html')
    else:
        return render(request, template_name='registration/invalid_link.html')

def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Password Reset Request"
                message = render_to_string("registration/password_reset_email.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': password_reset_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[associated_user.email])
                if email.send():
                    return render(request, template_name='registration/password_reset_done.html')
                else:
                    messages.error(request, "Problem sending reset password email, <b>SERVER PROBLEM</b>")
                    return redirect('home')

        for key, error in list(form.errors.items()):
            if key == 'captcha' and error[0] == 'This field is required.':
                messages.error(request, "You must pass the reCAPTCHA test")
                continue

    form = PasswordResetForm()
    return render(
        request=request,
        template_name="registration/password_reset_form.html",
        context={"form": form}
    )


def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    if user is not None and password_reset_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return render(request, template_name='registration/password_reset_complete.html')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = SetPasswordForm(user)
        return render(request, 'registration/password_reset_confirm.html', context={'form': form})
    else:
        messages.error(request, "Link is expired")

    messages.error(request, 'Something went wrong, redirecting back to Homepage')
    return redirect("home")


def booking(request):
    if request.user.is_authenticated:
        initial = {'name': request.user.first_name,
                   'surname': request.user.last_name,
                   'email': request.user.email}
    else:
        initial = {}
    if request.method == 'POST':
        form = BookingForm(request.POST, initial=initial)
        if form.is_valid():
            name = form.cleaned_data['name']
            surname = form.cleaned_data["surname"]
            email = form.cleaned_data['email']
            court = form.cleaned_data['court']
            coach = form.cleaned_data['coach']
            date = form.cleaned_data['date']
            hour = form.cleaned_data['hour']
            new_booking = Booking(name=name, surname=surname, email=email, court=court,
                                  coach=coach, date=date, hour=hour)
            new_booking.save()
            subject = "Succesful reservation"

            message = render_to_string('tennis/booking_email.html', {
                "name": name,
                "last_name": surname,
                "date": date,
                "hour": hour,
                "court": court,
                "coach": coach
            })
            e_mail = EmailMessage(subject, message, to=[email])
            if e_mail.send():
                return redirect('thanks')
            else:
                messages.error(request, "Problem saving your reservation, <b>SERVER PROBLEM</b>")
                return redirect('home')
    else:
        form = BookingForm(initial=initial)
    return render(request, 'tennis/booking.html', {'form': form})


def thanks(request):
    return render(request, 'tennis/thanks.html')


@login_required
def discount(request):
    discounts = Discounts.objects.all()
    context = {'discounts': discounts}
    return render(request, 'tennis/discounts.html', context=context)

@login_required
def updateBooking(request, pk):
    reser = Booking.objects.get(pk=pk)
    email = reser.email
    initial = {'name': reser.name,
               'surname': reser.surname,
               'court': reser.court,
               'coach': reser.coach,
               'date': reser.date,
               'hour': reser.hour}
    if request.method == 'POST':
        form = EditBooking(request.POST, initial=initial)
        if form.is_valid():
            reser.name = form.cleaned_data['name']
            reser.surname = form.cleaned_data['surname']
            reser.court = form.cleaned_data['court']
            reser.coach = form.cleaned_data['coach']
            reser.date = form.cleaned_data['date']
            reser.hour = form.cleaned_data['hour']
            reser.save()
            subject = "Succesful update of reservation"

            message = render_to_string('tennis/booking_email.html', {
                "name": form.cleaned_data['name'],
                "last_name": form.cleaned_data['surname'],
                "date":  form.cleaned_data['date'],
                "hour": form.cleaned_data['hour'],
                "court": form.cleaned_data['court'],
                "coach": form.cleaned_data['coach']
            })
            e_mail = EmailMessage(subject, message, to=[email])
            if e_mail.send():
                return redirect('thanks')
            else:
                messages.error(request, "Problem updating your reservation, <b>SERVER PROBLEM</b>")
                return redirect('home')
    else:
        form = EditBooking(initial=initial)
    return render(request, 'tennis/edit_booking.html', {'form': form})

@login_required
def deleteBooking(request, pk):
    reser = Booking.objects.get(pk=pk)
    if request.method == 'POST':
        form = DeleteBookingForm(request.POST)
        if form.is_valid():
            reser.delete()
            return redirect('profil')
    else:
        form = DeleteBookingForm()
    return render(request, template_name='tennis/delete_booking.html', context={'form': form})

