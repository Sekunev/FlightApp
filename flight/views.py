from django.shortcuts import render
from rest_framework import viewsets
from .serializers import FlightSerializer, ReservationSerializer, StaffFlightSerializer
from .models import Flight, Reservation
from rest_framework.permissions import IsAdminUser
from .permissions import IsStafforReadOnly
from datetime import datetime, date

# Create your views here.
class FlightView(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = (IsStafforReadOnly,)
    
    # Eğer kullanıcı admin ise (is_staff) StaffFlightSerializer çağırılarak uçuşlardaki rezervasyonların gösterimi sağlanması için.
    def get_serializer_class(self):
        serializer = super().get_serializer_class()
        if self.request.user.is_staff:
            return StaffFlightSerializer
        return serializer
    
    # Normal Kullanıcı Sadece gelecek uçuşları görmesi, admin kullanıcının ise tüm uçuşları görmesi için.
    def get_queryset(self):
        now = datetime.now() # Şimdiki Tarih
        current_time = now.strftime('%H:%M:%S')# Şimdiki saat
        today = date.today() # Bugün
        
        if self.request.user.is_staff:
            return super().get_queryset()  # Staff'sa hepsini gör (queryset = Flight.objects.all())
        
        else: # staff değilse filtrele.
            queryset = Flight.objects.filter(date_of_departure__gt=today)
            # date_of_departure büyükse bugünden demiş olduk --> (date_of_departure__gt=today)
            if Flight.objects.filter(date_of_departure=today): # date_of_departure bugünse
                today_qs = Flight.objects.filter(date_of_departure=today).filter(etd__gt=current_time)
                # today_qs = Mevcut zaman (current_time)'dan büyük olan (greater then) zamanlar. Gelecek zaman.

                queryset = queryset.union(today_qs)
                # union = Her iki kümedeki tüm öğeleri içeren bir küme döndürür, yinelenenler hariç tutulur: 
                # queryset ve today_qs leri birleştirdik.
            return queryset
    
    
class ReservationView(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    
    # ModelViewSet/GenericViewSet/GenericAPIView --> den def get_queryset(self): owerread yapıyoruz.
    # Neden? Frontend'den rezervasyolar GET edildiğinde admin ve normal kullanıcılar birlikte sergileniyor. Adminin tüm rezervasyonları normal kullanıcının ise sadece kendi rezervasyonlarını görebilmesi için filtreleme işlemi yapmamız gerekiyor.
    def get_queryset(self):
        queryset = super().get_queryset() # dinamik olması için yukardakinden farklı value oluşturuldu.
        #print(queryset) # <QuerySet [<Reservation: Reservation object (1)>, <Reservation: Reservation object (2)>, <Reservation: Reservation object (3)>, <Reservation: Reservation object (4)>, <Reservation: Reservation object (5)>, <Reservation: Reservation object (6)>, <Reservation: Reservation object (7)>, <Reservation: Reservation object (8)>]>

        #print(self.request.user) # AnonymousUser
        #print(self.request.user.id) # None
        #print(self.request.user) # <rest_framework.request.Request: GET '/flight/reservations/'>

        if self.request.user.is_staff:
            return queryset
        return queryset.filter(user = self.request.user)
    

