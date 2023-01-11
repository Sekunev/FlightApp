from rest_framework import serializers
from .models import Flight,Reservation, Passenger


class FlightSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Flight
        fields = (
            "id",
            "flight_number",
            "operation_airlines",
            "departure_city",
            "arrival_city",
            "date_of_departure",
            "etd"
        )
        
        
class PassengerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Passenger
        fields = "__all__"
  

class ReservationSerializer(serializers.ModelSerializer):

    passenger = PassengerSerializer(many=True, required=True)
    flight = serializers.StringRelatedField()  # __str__'deki ismi gelsin. read_only 
    flight_id = serializers.IntegerField(read_only=True) # create ederken str'ye çevirdiğimiz için(yukarıda) sorun yaşamamak için int'e çeviriyoruz. 
    user = serializers.StringRelatedField() # model tab. bulunan user'ide görmek istiyorum. ama str. olarak. 
    
    class Meta:
        model = Reservation
        fields = ("id", "flight", "flight_id", "user", "passenger")
        
    """#! Aşağıdaki create işlemini ne için yapıyoruz?
Frontend tarafından Gönderilen örnek bir post:
{
    "flight_id": 3,
    "passenger": [
        {
            "first_name": "jason2ds",
            "last_name": "derulo2ds",
            "email": "jaso2adn@test.com",
            "phone_number": 123761827845
        },
        {
            "first_name": "cooperdas2",
            "last_name": "henryds2",
            "email": "cop2pe@test.com",
            "phone_number": 3782424142
        }
    ]
}
    #  Frontend tarafından rezervasyon (post) işlemi yapıldığında "flight_id": 3'ün fligt tablosuna, passenger'ların ise passenger tablosuna gönderilmesi gerekiyor. Ama Reservation Tablosundaki passenger fieldi bulunmuyor. Nedeni Reservation Tablosundaki passenger'in manytomany ilişkiye sahip olması. Bu durumda Django flight_resrvation_passenger isimli bir tabloyu default olarak oluşturması. Bu sorunu ortadan kaldırmak için  passenger ayırma işlemini yapıyoruz. Yeni bir rezervasyon create ediyoruz. Liste türünde olan passenger_data'mızı for döngüsüne tabi tutarak her bir obje ile pasenger oluşturma işlemi yapıyoruz. Sonrasında bu iki objeyi birleştirerek kaydediyoruz. Kaydedilmiş objenin son halinide return ediyoruz."""

    def create(self, validated_data):
        # print(validated_data) # {'flight_id': 2, 'passenger': [OrderedDict([('first_name', 'jason2'), ('last_name', 'derulo2'), ('email', 'jaso2n@test.com'), ('phone_number', 1237618278)]), OrderedDict([('first_name', 'cooper2'), ('last_name', 'henry2'), ('email', 'cop2p@test.com'), ('phone_number', 378242412)])]}
        passenger_data = validated_data.pop("passenger")
        #print(passenger_data) # validated_data'dan passenger çıkarılmış hali # [OrderedDict([('first_name', 'jason2s'), ('last_name', 'derulo2s'), ('email', 'jaso2dn@test.com'), ('phone_number', 123761827845)]), OrderedDict([('first_name', 'cooperd2'), ('last_name', 'henryd2'), ('email', 'cop2p@test.com'), ('phone_number', 378242412)])]
        #print(validated_data) # {'flight_id': 3}
        validated_data["user_id"] = self.context["request"].user.id # istek atan user'a ulaşabiliyoruz. "self.context["request"].user.id" ile.
        # print(validated_data) # user_id i ekledik. {'flight_id': 3, 'user_id': 2}
        reservation = Reservation.objects.create(**validated_data) # rezervasyon create edioruz.
    
        for passenger in passenger_data:
            pas = Passenger.objects.create(**passenger) 
            # passenger_data 'daki her bir obje ile Passenger ccreate ediyoruz.
            reservation.passenger.add(pas) # reservation ların üzerine pas(Passenger)'leri ekleyerek birleştirme işlemi yapıyoruz.
        
        reservation.save()  # Birleştirdiğimiz objeyi kaydediyoruz.
        return reservation
        
        
# Flight'ler get edildiğinde hangi uçuşta hangi rezervasyonlar var bunu görebilmek için. aşağıdaki serializeri oluşturduk.     
class StaffFlightSerializer(serializers.ModelSerializer):
    
    reservation = ReservationSerializer(many=True, read_only=True)  # Bu field ismini modeldeki related_name'den aldı. Şimdi flight taplosunda sanki reservation fieldi varmış gibi bir durum oluştu. Bir uçuşun içerisinde birden fazla rezervasyon olacağı için many=True, uçuş create edilirken aynı zamanda rezervasyonda create edilmemesi için read_only=True yazdık.
    
    class Meta:
        model = Flight
        fields = (
            "id",
            "flight_number",
            "operation_airlines",
            "departure_city",
            "arrival_city",
            "date_of_departure",
            "etd",
            "reservation",
        )
        
        
    
    