from django.db import models
from django.contrib.auth.models import User, AbstractUser, Group
from rest_framework import serializers 
#from zone.models import Zone
from app.models import Zone
from app.models import Point
from app.models import MapForm
from app.models import ZoneParcelle
from app.models import PointParcelle
from app.models import MapFormParcelle
from app.models import TypeMachineEngins
from app.models import Machines_Tables
from app.models import Outils_Tables
from app.models import Carburants_Tables
from app.models import Pieces_Tables
from app.models import Rh_Tables
from app.models import Graine_Tables
from app.models import Traitement_Tables
from app.models import Engrais_Tables
#from app.models import Moteur_Tables
from app.models import Maison_Tables
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from datetime import datetime, timedelta
from rest_framework.serializers import ModelSerializer
from .models import User
from app.models import *
""" class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        
        data['username'] = user.username
        data['group'] = user.groups.first().name if user.groups.exists() else None
        data['permissions'] = [str(perm) for perm in user.user_permissions.all()]
        
        expiration_date = datetime.now() + timedelta(days=7)
        data['token_expires'] = expiration_date.strftime('%Y-%m-%d %H:%M:%S')
        
        return data """

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data['id'] = user.id
        data['group'] = user.groups.first().name if user.groups.exists() else None
        data['permissions'] = list(user.get_all_permissions())
        return data
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

        
class ZoneSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Zone
        fields = '__all__'
        
""" class UserProfileSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = UserProfile
        fields = '__all__'  """
        
class PointSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Point
        fields = '__all__'     
        
class FormSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = MapForm
        fields = '__all__'  
        
        
class ZoneParcelleSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = ZoneParcelle
        fields = '__all__'
        
class PointParcelleSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = PointParcelle
        fields = '__all__'     
        
class FormParcelleSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = MapFormParcelle
        fields = '__all__'         
        
class TypeMachineEngins(serializers.ModelSerializer):
    
    class Meta:
        model = TypeMachineEngins
        fields = '__all__'
        
class MachinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machines_Tables
        fields = '__all__'
        
class OutilsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outils_Tables
        fields = '__all__'
        
class CarburantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carburants_Tables
        fields = '__all__'
        
class PiecesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pieces_Tables
        fields = '__all__'
        
class RhSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rh_Tables
        fields = '__all__'
        
class GraineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Graine_Tables
        fields = '__all__'
        
class TraitementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Traitement_Tables
        fields = '__all__'
        
class EngraisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Engrais_Tables
        fields = '__all__'
        
class MaisonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maison_Tables
        fields = '__all__'
              
""" class MoteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moteur_Tables
        fields = '__all__' """
        
class OperationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = New_Oper_Tables
        fields = '__all__'