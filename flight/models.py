from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Flight(models.Model):
    flight_number = models.CharField(max_length=10)
    operation_airlines = models.CharField(max_length=15)
    departure_city = models.CharField(max_length=30)
    arrival_city = models.CharField(max_length=30)
    date_of_departure = models.DateField()
    etd = models.TimeField()

    def __str__(self):
        return f'{self.flight_number} - {self.departure_city} - {self.arrival_city}'

class Passenger(models.Model):  # cooper - jason - murat ... 
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()
    phone_number = models.IntegerField()
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

# Bir yolcu birden fazla rezerve yapabilir. bir rezerveye birden fazla yolcu eklenebilir. Her iki tablo da çoklu kayıt alabilir.

class Reservation(models.Model): #(cooper - murat)  - (cooper - jason) - () ....
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    passenger = models.ManyToManyField(Passenger, related_name="reservations") # Yolcu silindiğinde Reservation silinmeyeceği için on_delete yok. ManyToManyField ilişkisi olduğu için passenger fiel'i Reservation tablosunda görünmez. django default olarak Yeni bir tablo oluşturuyor.
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="reservation")

# related_name="" --> Parent'dan childe ulaşmak için kullanıyoruz. İsmini ne verdiysek o isim parentde bir field gibi oluyor.