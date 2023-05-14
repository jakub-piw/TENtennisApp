from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

hours = (
        ("10:00", ("10:00")),
        ("11:00", ("11:00")),
        ("12:00", ("12:00")),
        ("13:00", ("13:00")),
        ("14:00", ("14:00")),
        ("15:00", ("15:00")),
        ("16:00", ("16:00")),
        ("17:00", ("17:00")),
    )

User._meta.get_field('email')._unique = True
User._meta.get_field('username')._unique = True

class Court(models.Model):
    SCALE = (
        ("High", ("High")),
        ("Medium", ("Medium")),
        ("Low", ("Low")),
    )
    type = models.CharField(max_length=50)
    speed = models.CharField(choices=SCALE, max_length=30)
    bounce = models.CharField(choices=SCALE, max_length=30)
    description = models.TextField()
    photo = models.ImageField(upload_to ='static/images')

    def __str__(self):
        return self.type

class Trener(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    age = models.IntegerField()
    special = models.TextField()
    description = models.TextField()
    photo = models.ImageField(upload_to='static/images')

    def __str__(self):
        return self.name + " " + self.surname

class Booking(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    email = models.EmailField()
    court = models.ForeignKey(Court, models.CASCADE)
    coach = models.ForeignKey(Trener, models.CASCADE)
    date = models.DateField()
    hour = models.CharField(choices=hours, max_length=10)

    def get_absolute_url(self):
        return reverse('thanks')

class Discounts(models.Model):
    product_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    lower_price = models.DecimalField(max_digits=10, decimal_places=2)
    code = models.CharField(max_length=30)
    photo = models.ImageField(upload_to='static/images')
