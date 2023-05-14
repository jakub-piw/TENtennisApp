from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Court, Trener, hours
import re
import datetime


class NewUserForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)


    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.last_name = self.cleaned_data['last_name']
        user.first_name = self.cleaned_data['first_name']
        if commit:
            user.save()
        return user

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        pattern = re.compile("^[A-Z][a-z]+$")
        if not bool(pattern.match(first_name)):
            msg = 'Name must contain only letters and starts with a capital letter.'
            self.add_error('first_name', msg)

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        pattern = re.compile("^[A-Z][a-z]+$")
        if not bool(pattern.match(last_name)):
            msg = 'Last name must contain only letters and starts with a capital letter.'
            self.add_error('last_name', msg)

        return last_name


class BookingForm(forms.Form):
    name = forms.CharField(max_length=30)
    surname = forms.CharField(max_length=30)
    email = forms.EmailField()
    court = forms.ModelChoiceField(queryset=Court.objects.all())
    coach = forms.ModelChoiceField(queryset=Trener.objects.all())
    date = forms.DateField(widget=forms.SelectDateWidget())
    hour = forms.ChoiceField(choices=hours)

    def clean_name(self):
        name = self.cleaned_data['name']
        pattern = re.compile("^[A-Z][a-z]+$")
        if not bool(pattern.match(name)):
            msg = 'Name must contain only letters and starts with a capital letter.'
            self.add_error('name', msg)

        return name

    def clean_surname(self):
        surname = self.cleaned_data['surname']
        pattern = re.compile("^[A-Z][a-z]+$")
        if not bool(pattern.match(surname)):
            msg = 'Last name must contain only letters and starts with a capital letter.'
            self.add_error('surname', msg)

        return surname

    def clean_court(self):
        court = self.cleaned_data['court']
        courts = Court.objects.all()
        if court not in courts:
            msg = "Please choose preferred court type"
            self.add_error('court', msg)
        return court

    def clean_coach(self):
        coach = self.cleaned_data['coach']
        coaches = Trener.objects.all()
        if coach not in coaches:
            msg = "Please choose preferred coach"
            self.add_error('coach', msg)
        return coach

    def clean_date(self):
        date = self.cleaned_data['date']
        today = datetime.date.today()
        if date < today:
            msg = "Date of visit is incorrect"
            self.add_error('date', msg)

        return date

class EditBooking(BookingForm):
    email = None

class DeleteBookingForm(forms.Form):
    class Meta:
        fields = []





