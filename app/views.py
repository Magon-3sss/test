from django.conf import settings as conf_settings
from django.conf import settings
import base64
import io
import mimetypes
from uuid import uuid4
import uuid
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.http import HttpResponse, HttpResponseServerError, JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.tokens import default_token_generator 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login , logout
from django.contrib import messages
from django.core.serializers import serialize
#from rest_framework import serializers
#from django.core import serializers as core_serializers

from django.core.mail import send_mail, EmailMessage
from numpy import DataSource
from app.authentication import get_user_permissions
from noa import settings

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from app.models import Hangar_Tables, TypeHangerDepot, Zone
from app.serializers import CustomTokenObtainPairSerializer, ZoneSerializer
from app.serializers import PointSerializer
from app.serializers import FormSerializer
from app.models import MapForm
from app.models import Point
from app.models import TypeMachineEngins
from app.models import Machines_Tables
from app.models import Outils_Tables
from app.models import TypeOutilsAgricoles
from app.models import Carburants_Tables 
from app.models import TypeCarburant
from app.models import Pieces_Tables
from app.models import TypePieces
from app.models import Rh_Tables
from app.models import TypeRh
from app.models import Graine_Tables
from app.models import TypeGrainesPousses
from app.models import CategorieGrainesPousses
from app.models import Traitement_Tables
from app.models import TypeTraitement
from app.models import CategorieTraitement
from app.models import Engrais_Tables
from app.models import TypeEngrais
from app.models import CategorieEngrais
from app.models import Maison_Tables
from app.models import TypeMaisonVilla
#from app.models import Moteur_Tables
from app.models import TypeMoteur
from app.models import TypeCouplageMoteur
from app.models import TypeTensionMoteur
from app.models import ZoneParcelle
from app.models import PointParcelle
from app.models import MapFormParcelle 
from app.serializers import ZoneParcelleSerializer
from app.serializers import PointParcelleSerializer
from app.serializers import FormParcelleSerializer
from app.serializers import MachinesSerializer
from app.serializers import OutilsSerializer
from app.serializers import CarburantsSerializer
from app.serializers import PiecesSerializer
from app.serializers import RhSerializer
from app.serializers import GraineSerializer
from app.serializers import TraitementSerializer
from app.serializers import EngraisSerializer
#from app.serializers import MyTokenObtainPairSerializer
#from app.serializers import MoteurSerializer
from app.models import Filtre
from app.models import ColorReference
from django.views.decorators.csrf import csrf_exempt
import json
import requests 
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.tokens import default_token_generator
from app.permissions import custom_permissions
from django.contrib.auth import get_user_model
import jwt
from datetime import datetime, timedelta
from django.views.generic import TemplateView
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from app.models import *
from django.core.exceptions import ObjectDoesNotExist
from app.models import MapForm

from rest_framework.decorators import api_view
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from rest_framework.parsers import JSONParser 
from rest_framework import status, serializers, viewsets, routers
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import Token
from django.core.files.uploadedfile import InMemoryUploadedFile

""" def get_sidebar_content_based_on_group(request, user_group):
    if user_group == 'Basic':
        return render(request, 'app-sidebar.html')
    elif user_group == 'Regular':
        return render(request, 'app-sidebar.html')
    elif user_group == 'Premium':
        return render(request, 'app-sidebar.html')
    else:
        return 'Contenu par défaut'
def get_sidebar_content(request):
    user_group = request.COOKIES.get('userGroup', 'Default')
    print(user_group)  
    # Logique pour déterminer le contenu du sidebar en fonction du groupe d'utilisateur
    sidebar_content = get_sidebar_content_based_on_group(user_group)
    print(sidebar_content)
    return JsonResponse({'sidebar_content': sidebar_content}) """
    
def landing_page (request): 
    return render(request, 'landing-page.html')

def index(request):
    cookie = request.COOKIES.get('jwtToken')
    if cookie:
        user_group = request.COOKIES.get('userGroup') or None
        try:
            profile = request.user.profile
        except ObjectDoesNotExist:
            profile = None
        context = {
            'jwtToken': cookie,
            'userGroup': user_group,
            'profile_user': profile
        }
        print(context)
        return render(request, 'index.html', context)
    else:
        return render(request, 'signin.html')
class SidebarView(TemplateView):
    template_name = "app-sidebar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the user group
        user_group = self.request.user.groups.filter(name="Basic").first() or None

        # Conditionally show the menu items
        if user_group == "Basic":
            context["menu_items"] = [
                {"label": "Détection & Analyse"},
                {"label": "Settings"},
            ]
        elif user_group == "Regular":
            context["menu_items"] = [
                {"label": "Détection & Analyse"},
                {"label": "Aide à la décision"},
                {"label": "Réaction"},
                {"label": "Settings"},
            ]
        elif user_group == "Premium":
            context["menu_items"] = [
                {"label": "Détection & Analyse"},
                {"label": "Aide à la décision"},
                {"label": "Réaction"},
                {"label": "Manegement"},
                {"label": "Settings"},
            ]
        else:
            context["menu_items"] = [
                {"label": "Détection & Analyse"},
                {"label": "Aide à la décision"},
                {"label": "Réaction"},
                {"label": "Manegement"},
                {"label": "Reporting"},
                {"label": "IoT"},
                {"label": "Settings"},
            ]

        return context

""" @login_required
def your_view(request):
    user_groups = request.user.groups.all()
    context = {
        'user_groups': user_groups,
    }

    return render(request, 'index.html', context) """


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer 
    
""" class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer """ 
 
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username')

class UserAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user

    
""" def signout(request):
    if request.method =='POST':
        return JsonResponse({'status': 'test'}, status=status.HTTP_200_OK) """
     
def signout(request):
        logout(request)
        #messages.success(request, 'logout successfully!')
        response = redirect('about')
        response.delete_cookie('jwtToken')
        return response

def activate(request, uidb64, token):
    print("Calling check_token()...")
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        my_user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        my_user = None

    if my_user is not None and default_token_generator.check_token(my_user, token):
        my_user.is_active  = True        
        my_user.save()
        messages.success(request, "You are account is activated you can login by filling the form below.")
        return redirect("signin")
    else:
        messages.success(request, 'Activation failed please try again')
        return redirect('about')

""" Moteur """
@api_view(['POST'])
def save_moteur(request):
    if request.method =='POST':
        nom = request.POST.get('nom')
        marque = request.POST.get('marque')
        type_moteur = request.POST.get('type_moteur')
        puissance = request.POST.get('puissance')
        type_tension = request.POST.get('type_tension')
        tension = request.POST.get('tension')
        type_couplage = request.POST.get('type_couplage')
        courant = request.POST.get('courant')
        geozone = request.POST.get('geozone')
        print(nom)
        print(marque)
        print(type_moteur)
        print(puissance)
        print(type_tension)
        print(tension)
        print(type_couplage)
        print(courant)
        print(geozone)
        
        form = {
            "nom": nom,
            "marque": marque,
            "type_moteur": type_moteur,
            "puissance": puissance,
            "type_tension": type_tension,
            "tension": tension,
            "type_couplage": type_couplage,
            "courant": courant,
            "geozone": geozone
        }
        
        """ moteur_serializer = MoteurSerializer(data=form)
                
        if moteur_serializer.is_valid():
            print('yes')
            moteur_serializer.save()
            return JsonResponse(moteur_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('no')
            return JsonResponse({"Erreur": "Some error occured"}, status=status.HTTP_201_CREATED) """

""" Engrais """
@api_view(['POST'])
def save_engrai(request):
    if request.method == "POST":
        nom = request.POST.get('nom')
        type = request.POST.get('type_engrais')
        categorie = request.POST.get('categorie_engrais')
        composition = request.POST.get('composition')
        mode_utilisation = request.POST.get('mode-utilisation')
        dosage = request.POST.get('dosage')
        cout = request.POST.get('cout')
        quantite = request.POST.get('quantite')
        date_achat = request.POST.get('date_achat')
        description = request.POST.get('description')
        geozone = request.POST.get('geozone')
        if len(request.FILES) != 0:
                image = request.FILES['image']
        print(nom)
        print(type)
        print(categorie)
        print(composition)
        print(mode_utilisation)
        print(dosage)
        print(quantite)
        print(date_achat)
        print(description)
        print(image)
        
        form = {
                "nom": nom,
                "type": type,
                "categorie": categorie,
                "composition": composition,
                "mode_utilisation": mode_utilisation,
                "dosage": dosage,
                "cout": cout,
                "quantite": quantite,
                "date_achat": date_achat,
                "image": image,
                "geozone": geozone,
                "description": description
            }
        
        engrai_serializer = EngraisSerializer(data=form)
                
        if engrai_serializer.is_valid():
            print('yes')
            engrai_serializer.save()
            return JsonResponse(engrai_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('no')
            return JsonResponse({"Erreur": "Some error occured"}, status=status.HTTP_201_CREATED)

""" Traitements """
def traitements (request):
    list = []
    traitements = Traitement_Tables.objects.all()
    types_traitements = TypeTraitement.objects.all()
    categories_Traitements = CategorieTraitement.objects.all()
    projects = MapForm.objects.all()
    list.append({"types": types_traitements,"categories": categories_Traitements, "traitements":traitements, "projects": projects})
    return render(request, 'traitements.html', {'data': list})

@api_view(['POST'])
def save_traitement(request):
    if request.method == "POST":
        nom = request.POST.get('nom')
        type = request.POST.get('type_traitement')
        categorie = request.POST.get('categorie_traitement')
        composition = request.POST.get('composition')
        mode_utilisation = request.POST.get('mode-utilisation')
        dosage = request.POST.get('dosage')
        cout = request.POST.get('cout')
        quantite = request.POST.get('quantite')
        date_achat = request.POST.get('date_achat')
        description = request.POST.get('description')
        geozone = request.POST.get('geozone')
        if len(request.FILES) != 0:
                image = request.FILES['image']
        print(nom)
        print(type)
        print(categorie)
        print(composition)
        print(mode_utilisation)
        print(dosage)
        print(quantite)
        print(date_achat)
        print(description)
        print(image)
        
        form = {
                "nom": nom,
                "type": type,
                "categorie": categorie,
                "composition": composition,
                "mode_utilisation": mode_utilisation,
                "dosage": dosage,
                "cout": cout,
                "quantite": quantite,
                "date_achat": date_achat,
                "image": image,
                "geozone": geozone,
                "description": description
            }
        
        traitement_serializer = TraitementSerializer(data=form)
                
        if traitement_serializer.is_valid():
            print('yes')
            traitement_serializer.save()
            return JsonResponse(traitement_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('no')
            return JsonResponse({"Erreur": "Some error occured"}, status=status.HTTP_201_CREATED)

""" Graines et Pousses """
@api_view(['POST'])
def save_graine(request):
    if request.method == "POST":
        nom = request.POST.get('nom')
        type = request.POST.get('type_graines_pousses')
        categorie = request.POST.get('categorie_graines_pousses')
        origine = request.POST.get('origine')
        quantite = request.POST.get('quantite')
        cout = request.POST.get('cout')
        description = request.POST.get('description')
        geozone = request.POST.get('geozone')
        if len(request.FILES) != 0:
                image = request.FILES['image']
        print(nom)
        print(type)
        print(categorie)
        print(origine)
        print(quantite)
        print(cout)
        print(description)
        print(image)
        
        form = {
                "nom": nom,
                "type": type,
                "categorie": categorie,
                "origine": origine,
                "quantite": quantite,
                "cout": cout,
                "image": image,
                "geozone": geozone,
                "description": description
            }
        
        graine_serializer = GraineSerializer(data=form)
                
        if graine_serializer.is_valid():
            print('yes')
            graine_serializer.save()
            return JsonResponse(graine_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('no')
            return JsonResponse({"Erreur": "Some error occured"}, status=status.HTTP_201_CREATED)

""" Ressources Humaines"""
@api_view(['POST'])
def save_rh(request):
    if request.method == "POST":
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        type = request.POST.get('type_rh')
        adresse = request.POST.get('adresse')
        num_tel = request.POST.get('telephone')
        email = request.POST.get('email')
        fonction = request.POST.get('fonction')
        salaire_heure = request.POST.get('Salaire_heure')
        salaire_jour = request.POST.get('salaire_jour')
        salaire_mois = request.POST.get('salaire_mois')
        matricule_cnss = request.POST.get('matricule_cnss')
        date_contrat = request.POST.get('date_contrat')
        geozone = request.POST.get('geozone')
        if len(request.FILES) != 0:
                image = request.FILES['image']
        print(nom)
        print(prenom)
        print(type)
        print(adresse)
        print(num_tel)
        print(email)
        print(fonction)
        print(salaire_heure)
        print(salaire_jour)
        print(salaire_mois)
        print(matricule_cnss)
        print(image)
        print(date_contrat)
        
        form = {
                "nom": nom,
                "prenom": prenom,
                "type": type,
                "adresse": adresse,
                "num_tel": num_tel,
                "email": email,
                "fonction": fonction,
                "salaire_heure": salaire_heure,
                "salaire_jour": salaire_jour,
                "salaire_mois": salaire_mois,
                "matricule_cnss": matricule_cnss,
                "image": image,
                "date_contrat": date_contrat,
                "geozone": geozone
            }
        
        rh_serializer = RhSerializer(data=form)
                
        if rh_serializer.is_valid():
            print('yes')
            rh_serializer.save()
            return JsonResponse(rh_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('no')
            return JsonResponse({"Erreur": "Some error occured"}, status=status.HTTP_201_CREATED)

""" pieces de rechange """
@api_view(['POST'])
def save_pieces(request):
    if request.method == "POST":
        nom = request.POST.get('nom')
        type = request.POST.get('type_pieces')
        cout = request.POST.get('cout')
        date_achat = request.POST.get('date_achat')
        if len(request.FILES) != 0:
                image = request.FILES['image']
        print(nom)
        print(type)
        print(cout)
        print(date_achat)
        print(image)
        
        form = {
                "nom": nom,
                "type": type,
                "cout": cout,
                "date_achat": date_achat,
                "image": image
            }
        
        pieces_serializer = PiecesSerializer(data=form)
                
        if pieces_serializer.is_valid():
            print('yes')
            pieces_serializer.save()
            return JsonResponse(pieces_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('no')
            return JsonResponse({"Erreur": "Some error occured"}, status=status.HTTP_201_CREATED)

""" carburant """
@api_view(['POST'])
def save_carburant(request):
    if request.method == "POST":
        nom = request.POST.get('nom')
        type = request.POST.get('type_carburant')
        quantite = request.POST.get('quantite')
        cout = request.POST.get('cout')
        date_approvisionnement = request.POST.get('date_approvisionnement')
        print(nom)
        print(type)
        print(quantite)
        print(cout)
        print(date_approvisionnement)
        
        form = {
                "nom": nom,
                "type": type,
                "quantite": quantite,
                "cout": cout,
                "date_approvisionnement": date_approvisionnement
            }
        
        carburant_serializer = CarburantsSerializer(data=form)
                
        if carburant_serializer.is_valid():
            print('yes')
            carburant_serializer.save()
            return JsonResponse(carburant_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('no')
            return JsonResponse({"Erreur": "Some error occured"}, status=status.HTTP_201_CREATED) 


""" Outils Agricoles"""
@api_view(['POST'])
def save_outil(request):
    if request.method == "POST":
        allocation = ""
        type = request.POST.get('type_outils_agricoles')
        numero_de_serie = request.POST.get('numero_de_serie')
        marque = request.POST.get('marque')
        prix_location_heure = request.POST.get('prix_location_heure')
        prix_location_jour = request.POST.get('prix_location_jour')
        prix_location_mois = request.POST.get('prix_location_mois')
        date_location = request.POST.get('date_location')
        prix_achat = request.POST.get('prix_achat')
        date_achat = request.POST.get('date_achat')
        description = request.POST.get('description')
        if len(request.FILES) != 0:
                image = request.FILES['image']
                
        if(prix_achat and date_achat):
            allocation = "non"
        else:
            allocation = "oui"
        print(type)
        print(numero_de_serie)
        print(marque)
        print(prix_location_heure)
        print(prix_location_jour)
        print(prix_location_mois)
        print(date_location)
        print(prix_achat)
        print(date_achat)
        print(image)
        print(description)
        
        form = {
                "type": type,
                "numero_de_serie": numero_de_serie,
                "marque": marque,
                "prix_location_heure": prix_location_heure,
                "prix_location_jour": prix_location_jour,
                "prix_location_mois": prix_location_mois,
                "date_location": date_location,
                "prix_achat": prix_achat,
                "date_achat": date_achat,
                "image": image,
                "description": description,
                "allocation": allocation
            }
        
        outils_serializer = OutilsSerializer(data=form)
                
        if outils_serializer.is_valid():
            print('yes')
            outils_serializer.save()
            return JsonResponse(outils_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('no')
            return JsonResponse({"Erreur": "Some error occured"}, status=status.HTTP_201_CREATED) 

        
""" Machines & Engins """
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@permission_required('app.add_machines')
def save_machine(request):
     if request.method == "POST":
        user = request.user
        allowed_groups = ['Basic', 'Premium', 'Advanced']
        user_groups = user.groups.values_list('name', flat=True)
        if not any(group in user_groups for group in allowed_groups):
            return JsonResponse({"Erreur": "Vous n'avez pas la permission d'effectuer cette action"}, status=status.HTTP_403_FORBIDDEN)

        allocation = ""
        type = request.POST.get('type_machine_engins')
        matricule = request.POST.get('matricule')
        marque = request.POST.get('marque')
        carte_grise = request.POST.get('carte_grise')
        date_assurance = request.POST.get('date_assurance')
        date_visite = request.POST.get('date_visite')
        date_vignette = request.POST.get('date_vignette')
        prix_heure = request.POST.get('prix_heure')
        prix_jour = request.POST.get('prix_jour')
        prix_mois = request.POST.get('prix_mois')
        date_location = request.POST.get('date_location')
        prix_achat = request.POST.get('prix_achat')
        date_achat = request.POST.get('date_achat')
        description = request.POST.get('description')
        if len(request.FILES) != 0:
                image = request.FILES['image']

        if(prix_achat and date_achat):
            allocation = "non"
        else:
            allocation = "oui"           
        print(type)
        print(matricule)
        print(marque)
        print(carte_grise)
        print(date_assurance)
        print(date_visite)
        print(date_vignette)
        print(prix_heure)
        print(prix_jour)
        print(prix_mois)
        print(date_location)
        print(prix_achat)
        print(date_achat)
        print(image)
        print(description)
        
        form = {
                "type": type,
                "matricule": matricule,
                "marque": marque,
                "carte_grise": carte_grise,
                "date_assurance": date_assurance,
                "date_visite": date_visite,
                "date_vignette": date_vignette,
                "prix_heure": prix_heure,
                "prix_jour": prix_jour,
                "prix_mois": prix_mois,
                "date_location": date_location,
                "prix_achat": prix_achat,
                "date_achat": date_achat,
                "image": image,
                "description": description,
                "allocation": allocation
            }
        
        machines_serializer = MachinesSerializer(data=form)
                
        if machines_serializer.is_valid():
            print('yes')
            machines_serializer.save()
            return JsonResponse(machines_serializer.data, status=status.HTTP_200_OK)
        else:
            print('no')
            return JsonResponse({"Erreur": "Some error occured"}, status=status.HTTP_400_BAD_REQUEST)
             

""" Projects  """
@api_view(['POST'])    
def savezone(request):
   if request.method == 'POST':
        list = []
        geo_data = JSONParser().parse(request)
        #print(geo_data)
        # print(geo_data["type"])  
        tp = geo_data["type"]
        
        #print(tp)
        #coord = geo_data["coordinates"]
    
        if tp == "marker":
            
            coord = geo_data["coordinates"]
            xgeo = {
                "type": tp,
                "area": "No area for marker",
                "circle_radius": "No radius for marker"
            }
                
            type = json.dumps(xgeo)
            #print(type)
            
            zone_serializer = ZoneSerializer(data=xgeo)
            if zone_serializer.is_valid():
                print('yes')
                zone_serializer.save()
                res = zone_serializer.data
                print(res)
                id = res["id"]
                print(id)
                
            for x in coord:
                #print(x)
                list.append(x)
                #print(list)
            xcoordinates = {
                    "latt": str(list[1]),
                    "long": str(list[0]),
                    "geozone": id
                }
            print(xcoordinates)  
            
            dupedcoord = json.dumps(xcoordinates)
            
            coordinates = json.loads(dupedcoord)
            
            point_serializer = PointSerializer(data=coordinates)
            print(point_serializer)
            if point_serializer.is_valid():
                point_serializer.save()
            return JsonResponse(zone_serializer.data, status=status.HTTP_201_CREATED)#zone_serializer.data
        if tp == "polyline":
            coord = geo_data["coordinates"]
            xgeo = {
                "type": tp,
                "area": "No area for polyline",
                "circle_radius": "No radius for polyline"
            }
                
            type = json.dumps(xgeo)
            print(type)
            
            zone_serializer = ZoneSerializer(data=xgeo)
            if zone_serializer.is_valid():
                print('yes')
                zone_serializer.save()
                res = zone_serializer.data
                print(res)
                id = res["id"]
                print(id)
            for level1 in coord:
                print(level1)
                list = level1
                
                xcoordinates = {
                        "latt": str(list[1]),
                        "long": str(list[0]),
                        "geozone": id
                    }
                print(xcoordinates)  
                
                dupedcoord = json.dumps(xcoordinates)
                
                coordinates = json.loads(dupedcoord)
                
                point_serializer = PointSerializer(data=coordinates)
                if point_serializer.is_valid():
                    point_serializer.save()
            return JsonResponse(zone_serializer.data, status=status.HTTP_201_CREATED)  
        if tp == "polygon":
            area = geo_data["area"]
            coord = geo_data["coordinates"]
            xgeo = {
                "type": tp,
                "area": area,
                "circle_radius": "No radius for polygon"
            }
                
            type = json.dumps(xgeo)
            print(type)
            
            zone_serializer = ZoneSerializer(data=xgeo)
            if zone_serializer.is_valid():
                print('yes')
                zone_serializer.save()
                res = zone_serializer.data
                print(res)
                id = res["id"]
                print(id)
            for level1 in coord:
                print(level1)
                for level2 in level1:
                    print(level2)
                    list = level2
                
                    xcoordinates = {
                            "latt": str(list[1]),
                            "long": str(list[0]),
                            "geozone": id
                        }
                    print(xcoordinates)  
                    
                    dupedcoord = json.dumps(xcoordinates)
                    
                    coordinates = json.loads(dupedcoord)
                    
                    point_serializer = PointSerializer(data=coordinates)
                    if point_serializer.is_valid():
                        point_serializer.save()
                return JsonResponse(zone_serializer.data, status=status.HTTP_201_CREATED) 
        if tp == "rectangle":
            area = geo_data["area"]
            coord = geo_data["coordinates"]
            xgeo = {
                "type": tp,
                "area": area,
                "circle_radius": "No radius for rectangle"
            }
                
            type = json.dumps(xgeo)
            print(type)
            
            zone_serializer = ZoneSerializer(data=xgeo)
            if zone_serializer.is_valid():
                print('yes')
                zone_serializer.save()
                res = zone_serializer.data
                print(res)
                id = res["id"]
                print(id)
            for level1 in coord:
                print(level1)
                for level2 in level1:
                    print(level2)
                    list = level2
                
                    xcoordinates = {
                            "latt": str(list[1]),
                            "long": str(list[0]),
                            "geozone": id
                        }
                    print(xcoordinates)  
                    
                    dupedcoord = json.dumps(xcoordinates)
                    
                    coordinates = json.loads(dupedcoord)
                    
                    point_serializer = PointSerializer(data=coordinates)
                    if point_serializer.is_valid():
                        point_serializer.save()
                return JsonResponse(zone_serializer.data, status=status.HTTP_201_CREATED)
        if tp == "circle":
            radius = geo_data["circle_radius"]
            area = geo_data["area"]
            coord = geo_data["coordinates"]
            xgeo = {
                "type": tp,
                "area": area,
                "circle_radius": radius
            }
                
            type = json.dumps(xgeo)
            print(type)
            
            zone_serializer = ZoneSerializer(data=xgeo)
            if zone_serializer.is_valid():
                print('yes')
                zone_serializer.save()
                res = zone_serializer.data
                print(res)
                id = res["id"]
                print(id)
        
            for x in coord:
                    print(x)
                    list.append(x)
                    print(list)
            xcoordinates = {
                        "latt": str(list[1]),
                        "long": str(list[0]),
                        "geozone": id
                    }
            print(xcoordinates)  
            
            dupedcoord = json.dumps(xcoordinates)
            
            coordinates = json.loads(dupedcoord)
            
            point_serializer = PointSerializer(data=coordinates)
            if point_serializer.is_valid():
                point_serializer.save()
            return JsonResponse(zone_serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def save_form(request):
     if request.method == "POST":
        form = JSONParser().parse(request)
        print(form)
        form_serializer = FormSerializer(data=form)
        if form_serializer.is_valid():
            print('yes')
            form_serializer.save()
            return JsonResponse(form_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('no')
            return JsonResponse({"Erreur": "Some error occured"}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_zone(request, pk):
    # ... tutorial = Tutorial.objects.get(pk=pk)
 
    if request.method == 'GET': 
          try: 
            zone = Zone.objects.get(pk=pk) 
            zone_serializer = ZoneSerializer(zone) 
            return JsonResponse(zone_serializer.data) 
          except Zone.DoesNotExist: 
            return JsonResponse({"msg": "erreur"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
       
@api_view(['GET'])
def get_point(request, pk):
    if request.method == "GET":
        try:
            zone = Zone.objects.get(pk=pk) 
            zone_serializer = ZoneSerializer(zone)
            p = serializers.serialize("json", Point.objects.all().filter(geozone=pk))
            z = zone_serializer.data
            print(p)
            tp =  z["type"]
            print(tp)
            radius = z["circle_radius"]
            print(radius)
            if tp == "circle":
                 context = {
                'type': tp,
                'radius': radius,
                'points': p,
                }
                 
            if tp == "polygon" or tp == "rectangle":
                 context = {
                'type': tp,
                'points': p,
                }
            if tp == "polyline":
                 context = {
                'type': tp,
                'points': p,
                }
            if tp == "marker":
                 context = {
                'type': tp,
                'points': p,
                }
            data = json.dumps(context, indent=4, sort_keys=True, default=str)
            return HttpResponse(data, content_type='application/json', status=status.HTTP_200_OK)
            """ if zone_serializer.is_valid():
                return JsonResponse(zone_serializer.data,p,status=status.HTTP_200_OK, safe=False) """#{"msg": "point"}
        except Point.DoesNotExist:
            return JsonResponse({"msg": "erreur"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR )

""" Parcelles """         
@api_view(['POST'])    
def savezoneparcelle(request):
   if request.method == 'POST':
        existanceIdProjet = True
        list = []
        geo_data = JSONParser().parse(request)
     
        tp = geo_data["type"]
        print(tp)
        id_projet = geo_data["id_projet"]
        print("id projet : ",id_projet)
        
        #coord = geo_data["coordinates"]
    
        if tp == "marker":
            
            coord = geo_data["coordinates"]
           
            xgeo = {
                "type": tp,
                "area": "No area for marker",
                "circle_radius": "No radius for marker",
                "id_projet": id_projet
            }
                
            type = json.dumps(xgeo)
            print(type)
            
            Zone_Parcelle_serializer = ZoneParcelleSerializer(data=xgeo)
            if Zone_Parcelle_serializer.is_valid():
                print('yes')
                Zone_Parcelle_serializer.save()
                res = Zone_Parcelle_serializer.data
                print(res)
                id = res["id"]
                print(id)
                
            for x in coord:
                print(x)
                list.append(x)
                print(list)
            xcoordinates = {
                    "latt": str(list[1]),
                    "long": str(list[0]),
                    "geozone": id
                }
            print(xcoordinates)  
            
            dupedcoord = json.dumps(xcoordinates)
            
            coordinates = json.loads(dupedcoord)
            print(coordinates)
            point_parcelle_serializer = PointParcelleSerializer(data=coordinates)
            print(point_parcelle_serializer)
            if point_parcelle_serializer.is_valid():
                print('valid')
                point_parcelle_serializer.save()
            else:
                print('not valid')
            return JsonResponse(Zone_Parcelle_serializer.data, status=status.HTTP_201_CREATED)
        if tp == "polyline":
            coord = geo_data["coordinates"]
            xgeo = {
                "type": tp,
                "area": "No area for polyline",
                "circle_radius": "No radius for polyline",
                "id_projet": id_projet
            }
                
            type = json.dumps(xgeo)
            print(type)
            
            Zone_Parcelle_serializer = ZoneParcelleSerializer(data=xgeo)
            if Zone_Parcelle_serializer.is_valid():
                print('yes')
                Zone_Parcelle_serializer.save()
                res = Zone_Parcelle_serializer.data
                print(res)
                id = res["id"]
                print(id)
            for level1 in coord:
                print(level1)
                list = level1
                
                xcoordinates = {
                        "latt": str(list[1]),
                        "long": str(list[0]),
                        "geozone": id
                    }
                print(xcoordinates)  
                
                dupedcoord = json.dumps(xcoordinates)
                
                coordinates = json.loads(dupedcoord)
                
                point_parcelle_serializer = PointParcelleSerializer(data=coordinates)
                if point_parcelle_serializer.is_valid():
                    point_parcelle_serializer.save()
            return JsonResponse(Zone_Parcelle_serializer.data, status=status.HTTP_201_CREATED)  
        if tp == "polygon":
            area = geo_data["area"]
            coord = geo_data["coordinates"]
            if id_projet == "":
                id_projet = "Pracel without project"
            xgeo = {
                "type": tp,
                "area": area,
                "circle_radius": "No radius for polygon",
                "id_projet": id_projet
            }
                
            type = json.dumps(xgeo)
            print(type)
            
            Zone_Parcelle_serializer = ZoneParcelleSerializer(data=xgeo)
            if Zone_Parcelle_serializer.is_valid():
                print('yes')
                Zone_Parcelle_serializer.save()
                res = Zone_Parcelle_serializer.data
                print(res)
                id = res["id"]
                print(id)
            else:
                print('nooooooo')
            for level1 in coord:
                print(level1)
                for level2 in level1:
                    print(level2)
                    list = level2
                
                    xcoordinates = {
                            "latt": str(list[1]),
                            "long": str(list[0]),
                            "geozone": id
                        }
                    print(xcoordinates)  
                    
                    dupedcoord = json.dumps(xcoordinates)
                    
                    coordinates = json.loads(dupedcoord)
                    
                    point_parcelle_serializer = PointParcelleSerializer(data=coordinates)
                    if point_parcelle_serializer.is_valid():
                        point_parcelle_serializer.save()
                return JsonResponse(Zone_Parcelle_serializer.data, status=status.HTTP_201_CREATED) 
        if tp == "rectangle":
            area = geo_data["area"]
            coord = geo_data["coordinates"]
            xgeo = {
                "type": tp,
                "area": area,
                "circle_radius": "No radius for rectangle",
                "id_projet": id_projet
            }
                
            type = json.dumps(xgeo)
            print(type)
            
            Zone_Parcelle_serializer = ZoneParcelleSerializer(data=xgeo)
            if Zone_Parcelle_serializer.is_valid():
                print('yes')
                Zone_Parcelle_serializer.save()
                res = Zone_Parcelle_serializer.data
                print(res)
                id = res["id"]
                print(id)
            for level1 in coord:
                print(level1)
                for level2 in level1:
                    print(level2)
                    list = level2
                
                    xcoordinates = {
                            "latt": str(list[1]),
                            "long": str(list[0]),
                            "geozone": id
                        }
                    print(xcoordinates)  
                    
                    dupedcoord = json.dumps(xcoordinates)
                    
                    coordinates = json.loads(dupedcoord)
                    
                    point_parcelle_serializer = PointParcelleSerializer(data=coordinates)
                    if point_parcelle_serializer.is_valid():
                        point_parcelle_serializer.save()
                return JsonResponse(Zone_Parcelle_serializer.data, status=status.HTTP_201_CREATED)
        if tp == "circle":
            radius = geo_data["circle_radius"]
            area = geo_data["area"]
            coord = geo_data["coordinates"]
            xgeo = {
                "type": tp,
                "area": area,
                "circle_radius": radius,
                "id_projet": id_projet
            }
                
            type = json.dumps(xgeo)
            print(type)
            
            Zone_Parcelle_serializer = ZoneParcelleSerializer(data=xgeo)
            if Zone_Parcelle_serializer.is_valid():
                print('yes')
                Zone_Parcelle_serializer.save()
                res = Zone_Parcelle_serializer.data
                print(res)
                id = res["id"]
                print(id)
        
            for x in coord:
                    print(x)
                    list.append(x)
                    print(list)
            xcoordinates = {
                        "latt": str(list[1]),
                        "long": str(list[0]),
                        "geozone": id
                    }
            print(xcoordinates)  
            
            dupedcoord = json.dumps(xcoordinates)
            
            coordinates = json.loads(dupedcoord)
            
            point_parcelle_serializer = PointParcelleSerializer(data=coordinates)
            if point_parcelle_serializer.is_valid():
                point_parcelle_serializer.save()
            return JsonResponse(Zone_Parcelle_serializer.data, status=status.HTTP_201_CREATED) 

@api_view(['POST'])
def save_form_parcelle(request):
     if request.method == "POST":
        form = JSONParser().parse(request)
        print(form)
        form_parcelle_serializer = FormParcelleSerializer(data=form)
        if form_parcelle_serializer.is_valid():
            print('yes')
            form_parcelle_serializer.save()
            return JsonResponse(form_parcelle_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('no')
            return JsonResponse({"Erreur": "Some error occured"}, status=status.HTTP_201_CREATED)
           
########################################################################
""" from django.http import HttpResponse
from .sentinel_hub import get_true_color_image
from sentinelhub import CRS, BBox
from sentinelhub import SHConfig 

def sentinel_hub_view(request):
    bbox = (13.37, 52.52, 13.38, 52.53)  # Remplacez par vos coordonnées réelles
    bbox_object = BBox(bbox, crs=CRS.WGS84)
    time_interval = ("2020-06-01", "2020-06-30")
    image = get_true_color_image(bbox=bbox_object, time_interval=time_interval)

    response = HttpResponse(content_type="image/jpeg")
    response.write(image)

    return HttpResponse(image, content_type="image/png") """

""" def sentinelhub_api_example(request):
    # Replace 'your_access_token' with your actual Sentinel Hub access token
    access_token = 'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJ3dE9hV1o2aFJJeUowbGlsYXctcWd4NzlUdm1hX3ZKZlNuMW1WNm5HX0tVIn0.eyJleHAiOjE3MDY2OTE5MDksImlhdCI6MTcwNjY4ODMwOSwianRpIjoiOGRlYzExMTAtNDkwZi00MjFlLTlkMzQtYjQ2ODgwNTJkM2UwIiwiaXNzIjoiaHR0cHM6Ly9zZXJ2aWNlcy5zZW50aW5lbC1odWIuY29tL2F1dGgvcmVhbG1zL21haW4iLCJzdWIiOiI0NjEyMGQ0Yy03MGVhLTQzZDktOGVmMy02NDVjNGY0MTNkNWIiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiIwZGI2M2Q3MS0wMGMyLTQ2NzYtOTgzNi04NGJiYWRjZTNkNGQiLCJzY29wZSI6ImVtYWlsIHByb2ZpbGUiLCJjbGllbnRIb3N0IjoiMTk3LjUuMTI5LjYiLCJjbGllbnRJZCI6IjBkYjYzZDcxLTAwYzItNDY3Ni05ODM2LTg0YmJhZGNlM2Q0ZCIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwicHJlZmVycmVkX3VzZXJuYW1lIjoic2VydmljZS1hY2NvdW50LTBkYjYzZDcxLTAwYzItNDY3Ni05ODM2LTg0YmJhZGNlM2Q0ZCIsImNsaWVudEFkZHJlc3MiOiIxOTcuNS4xMjkuNiIsImFjY291bnQiOiI1OTRjMDU5MC0zYTdlLTRjMGUtYTg4Zi0yN2U0MmVlOThjNDEifQ.exvRDify7w4luuBFZAzMPYQZkXST9KImbr23a1mBCk9T3e003XMpO_QOd-6E9EAxkiZIKfHSBh6ZdWYeeeBbJO6cNwlDSEsyUP1J9uuG56EFB5fuHWTAM5t1sMF1D_TvtGj6-gpldg4KhEvqq37d7ip_mMi2_8b586x_f_YT26trA0I9EP5I-uAJIY19EKcmWfkR94zFedbt9OUFnS5xlX9z3d_Pm3iLDFoLGeuO9wBKHIwRSfQEns6Ce4UZKztgmV9-Unu0NSBlOONqSE8YniB3EbTOalF2U_P3QKzdheOK84FhWSssbNsRzO0eVHS9ezEpLC4TKgZ1S2EkpVRMnQ'

    # Define the API endpoint
    api_url = 'https://services.sentinel-hub.com/api/v1/process'
    

    # Define the headers and payload
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }

    # Define the input payload
    input_payload = {
        "bounds": {
            "properties": {
                "crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [-94.04798984527588, 41.7930725281021],
                            [-94.04803276062012, 41.805773608962869],
                            [-94.06738758087158, 41.805901566741308],
                            [-94.06734466552735, 41.7967199475024],
                            [-94.06223773956299, 41.79144072064381],
                            [-94.0504789352417, 41.791376727347969],
                            [-94.05039310455322, 41.7930725281021],
                            [-94.04798984527588, 41.7930725281021]
                    ]
                ]
            }
        },
        "data": [
            {
                "type": "sentinel-2-l1c",
                "dataFilter": {
                    "timeRange": {
                        "from": "2020-10-01T00:00:00Z",
                        "to": "2022-10-31T00:00:00Z"
                    }
                }
            }
        ]
    }

    # Define the output payload
    output_payload = {
        "width": 512,
        "height": 512,
        "responses": [
            {
                "identifier": "default",
                "format": {
                    "type": "image/jpeg",
                    "quality": 80
                }
            }
        ]
    }

    # Define the Evalscript
    evalscript = '''
        //VERSION=3
        function setup() {
          return {
            input: [{
              bands:["B04", "B08", "dataMask"],
            }],
            output: {
              id: "default",
              bands: 4,
            }
          }
        }

        function evaluatePixel(sample) {
                let ndvi = (sample.B08 - sample.B04) / (sample.B08 + sample.B04)
                if (sample.dataMask == 1){
                    
                    
                    if (ndvi<-0.5) return [0.05,0.05,0.05, 1]
                    else if (ndvi<-0.2) return [0.75,0.75,0.75, 1]
                    else if (ndvi<-0.1) return [0.86,0.86,0.86, 1]
                    else if (ndvi<0) return [0.92,0.92,0.92, 1]
                    else if (ndvi<0.025) return [1,0.98,0.8, 1]
                    else if (ndvi<0.05) return [0.93,0.91,0.71, 1]
                    else if (ndvi<0.075) return [0.87,0.85,0.61, 1]
                    else if (ndvi<0.1) return [0.8,0.78,0.51, 1]
                    else if (ndvi<0.125) return [0.74,0.72,0.42, 1]
                    else if (ndvi<0.15) return [0.69,0.76,0.38, 1]
                    else if (ndvi<0.175) return [0.64,0.8,0.35, 1]
                    else if (ndvi<0.2) return [0.57,0.75,0.32, 1]
                    else if (ndvi<0.25) return [0.5,0.7,0.28, 1]
                    else if (ndvi<0.3) return [0.44,0.64,0.25, 1]
                    else if (ndvi<0.35) return [0.38,0.59,0.21, 1]
                    else if (ndvi<0.4) return [0.31,0.54,0.18, 1]
                    else if (ndvi<0.45) return [0.25,0.49,0.14, 1]
                    else if (ndvi<0.5) return [0.19,0.43,0.11, 1]
                    else if (ndvi<0.55) return [0.13,0.38,0.07, 1]
                    else if (ndvi<0.6) return [0.06,0.33,0.04, 1]
                    else if (ndvi==0) return [1, 1, 1, 1]
                    else return [0,0.27,0, 1]
                }
                else{
                    return [1, 1, 1, 0]
                } 
        } 
    '''

    # Create the complete payload
    payload = {
        'input': input_payload,
        'output': output_payload,
        'evalscript': evalscript
    }

    # Make the API request
    response = requests.post(
        api_url,
        headers=headers,
        json=payload
    )
    # Check if the response is successful (status code 200) and content is an image
    if response.status_code == 200 and response.headers.get('Content-Type') == 'image/jpeg':
        # Return the image directly
        return HttpResponse(response.content, content_type='image/jpeg')
   
    # Handle the API response (you may want to parse and display the results)
    try:
        result = response.json()
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        result = {'error': {'status': response.status_code, 'message': 'Invalid JSON response'}}
    #encoded_image = base64.b64encode(image_data).decode('utf-8')
    return render(request, 'sentinelhub_result.html', {'result': result}) """

###############################################################################
###############################################################################
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from sentinelhub import SentinelHubRequest, CRS, BBox, DataCollection, Geometry
from sentinelhub import SHConfig
from django.views.decorators.http import require_POST
from PIL import Image
import datetime
import os
import traceback

import numpy as np
from sentinelhub import MimeType

# Configuration de Sentinel Hub
config = SHConfig()
config.instance_id = "211dc98f-d4d3-4229-b540-703e8f0b8d9b"
if not config.sh_client_id or not config.sh_client_secret:
  config.sh_client_id = 'b75db3ae-30a5-4be2-a920-c5ea4973df49'
  config.sh_client_secret = 'jORm8qGiwWy1VZgidGyyGapYsap19A0b'
from shapely.geometry import Polygon


def create_mask_geometry(points):
  polygon = Polygon(points)
  mask_geometry = Geometry(geometry=polygon, crs=CRS.WGS84)
  return mask_geometry

@require_POST
@api_view(['POST'])
@csrf_exempt
def generate_raster_image(request):
  if request.method == "POST":
    data = request.data
    date = data["date"]
    points = data["points"]
    filtre_value = data.get("filtre")
    data_folder="D:/MAGON_3SSS/MAGON_3SSS/MAGON_3SSS-main/MAGON_3S/static/assets/sentinel"
    folder_name = str(uuid.uuid4())
    folder_path = os.path.join(data_folder, folder_name)
    if not os.path.exists(folder_path):
      os.makedirs(folder_path)
    evalscript = get_evalscript(filtre_value)
    bbox = create_bbox([(p[0], p[1]) for p in points])
    mask_geometry = create_mask_geometry([(p[0], p[1]) for p in points])
    sh_request = SentinelHubRequest(
    data_folder=folder_path,
    evalscript=evalscript,
    geometry=mask_geometry,
    input_data=[
      SentinelHubRequest.input_data(
        data_collection=DataCollection.SENTINEL2_L2A,
        time_interval=(date, date),
      )
    ],
    responses=[SentinelHubRequest.output_response("default", "png")],
    bbox=bbox,
    size=(512,512), 
    config=config,
    )
  image_path = os.path.join(folder_path, "response.png")
  print(f"Image path: {image_path}")
  try:
    response = sh_request.get_data(save_data=True)  
    image_bytes = response[0] if response else None
    files = os.listdir(folder_path)
    sub_folder = [f for f in files if os.path.isdir(os.path.join(folder_path, f))][0]
    folder_with_image = os.path.join(folder_path, sub_folder)
    if image_bytes is None:
      raise ValueError("No image data received from SentinelHub.")
    image_url = request.build_absolute_uri(f'/static/assets/sentinel/{folder_with_image}/response.png')
    #image_url = request.build_absolute_uri(f'/static/assets/sentinel/{date}_response/response.png')

    #image_url = f"/static/assets/sentinel/{date}_response/response.png"
    #image_url = f"{data_folder}/{folder_name}/response.png"
    return JsonResponse({"image_url": image_url})
    #return JsonResponse({"image_url": "/static/assets/sentinel/2b8105841735d27341cdf126b3a4c6b6/response.png"})
  except Exception as e:
    print("Erreur lors de la récupération des données : ", str(e))
    return JsonResponse({"error": str(e)}, status=500)

# Fonction d'extraction des coordonnées
def extract_coordinates(points):
  coordinates = []
  for p in points:
    try:
      lang = float(p["long"])  
      latt = float(p["latt"])  
      coordinates.append([lang, latt])
    except (ValueError, KeyError, TypeError):
      return []  
  return coordinates

def create_bbox(coordinates):
  min_lng = min(coord[0] for coord in coordinates)
  max_lng = max(coord[0] for coord in coordinates)
  min_lat = min(coord[1] for coord in coordinates)
  max_lat = max(coord[1] for coord in coordinates)
   
  bbox = BBox(bbox=[(min_lng, min_lat), (max_lng, max_lat)], crs=CRS.WGS84)
  print("BBox créée : ", repr(bbox))
  return bbox

# Fonction de génération du script Evalscript
def get_evalscript(filtre_value):
  if filtre_value == "NDVI":
    return """
      //VERSION=3
function setup() {
   return {
      input: ["B04", "B08", "dataMask"],
      output: { bands: 4 }
   };
}

const ramp = [
   [-1, 0xC5142A],
   [0.05, 0xC5142A],
   [0.1, 0xC5142A],
   [0.15, 0xE02D2C],
   [0.2, 0xEF4C3A],
   [0.25, 0xFE6C4A],
   [0.3, 0xFF8D5A],
   [0.35, 0xFFAB69],
   [0.4, 0xFFC67D],
   [0.45, 0xFFE093],
   [0.5, 0xFFEFAB],
   [0.55, 0xFDFEC2],
   [0.6, 0xEAF7AC],
   [0.65, 0xD5EF94],
   [0.7, 0xB9E383],
   [0.75, 0x9BD873],
   [0.8, 0x77CA6F],
   [0.85, 0x53BD6B],
   [0.9, 0x14AA60],
   [0.95, 0x009755],
   [1, 0x007E47],
];

const visualizer = new ColorRampVisualizer(ramp);

function evaluatePixel(samples) {
   let ndvi = index(samples.B08, samples.B04);
   let imgVals = visualizer.process(ndvi);
   return imgVals.concat(samples.dataMask)
}
    """
  elif filtre_value == "NDRE":
    return """
      //VERSION=3
function setup() {
   return {
      input: ["B05", "B08", "dataMask"],
      output: { bands: 4 }
   };
}

const ramp = [
   [-1, 0xC5142A],
   [0.05, 0xC5142A],
   [0.1, 0xC5142A],
   [0.15, 0xE02D2C],
   [0.2, 0xEF4C3A],
   [0.25, 0xFE6C4A],
   [0.3, 0xFF8D5A],
   [0.35, 0xFFAB69],
   [0.4, 0xFFC67D],
   [0.45, 0xFFE093],
   [0.5, 0xFFEFAB],
   [0.55, 0xFDFEC2],
   [0.6, 0xEAF7AC],
   [0.65, 0xD5EF94],
   [0.7, 0xB9E383],
   [0.75, 0x9BD873],
   [0.8, 0x77CA6F],
   [0.85, 0x53BD6B],
   [0.9, 0x14AA60],
   [0.95, 0x009755],
   [1, 0x007E47],
];

const visualizer = new ColorRampVisualizer(ramp);

function evaluatePixel(samples) {
   let ndre = index(samples.B08, samples.B05);
   let imgVals = visualizer.process(ndre);
   return imgVals.concat(samples.dataMask)
}
    """
  elif filtre_value == "SAVI":
    return """
      //VERSION=3
        let viz = ColorGradientVisualizer.createBlueRed();

        function evaluatePixel(samples) {
            let val = 1.5 * (samples.B08 - samples.B04) / (samples.B08 + samples.B04 + 0.5);
            val = viz.process(val);
            val.push(samples.dataMask);
            return val;
        }

        function setup() {
        return {
            input: [{
            bands: [
                "B04",
                "B08",
                "dataMask"
            ]
            }],
            output: {
            bands: 4
            }
        }
        }
    """
  elif filtre_value == "MSAVI 2":
    return """
      //VERSION=3

// Créez une instance de ColorRampVisualizer avec les rampes de couleur
const moistureRamps = [
    [1, 0x004728],
    [0.7, 0x005530],
    [0.6, 0x00673A],
    [0.5, 0x007E47],
    [0.4, 0x009755],
    [0.35, 0x14AA60],
    [0.3, 0x53BD6B],
    [0.27, 0x77CA6F],
    [0.25, 0x9BD873],
    [0.22, 0xB9E383],
    [0.17, 0xEAF7AC],
    [0.15, 0xFDFEC2],
    [0.12, 0xFFEFAB],
    [0.10, 0xFFE093],
    [0.8, 0xFFC67D],
    [0.6, 0xFFAB69],
    [0.4, 0xFF8D5A],
    [0.2, 0xFE6C4A],
    [0, 0xAD0028],
    [-1, 0xAD0028]
];

let viz = new ColorRampVisualizer(moistureRamps);

function evaluatePixel(samples) {
    let a = 2.0 * samples.B08 - 1.0;
    let val = (samples.B08 + 1.0) - 0.5 * Math.sqrt(a * a + 8.0 * samples.B04);
    val = viz.process(val);
    val.push(samples.dataMask);
    return val;
}

function setup() {
  return {
    input: [{
      bands: [
        "B04",
        "B08",
        "dataMask"
      ]
    }],
    output: {
      bands: 4
    }
  }
}

    """
  elif filtre_value == "NDMI":
    return """
      //VERSION=3
function setup() {
    return {
        input: ["B08", "B11", "dataMask"],
        output: { bands: 4 }
    };
}

// Define the color ramp with proper intervals
const moistureRamps = [
    [1, 0x0F30DE],
    [0.9, 0x213DDD],
    [0.8, 0x3249DC],
    [0.7, 0x4356DB],
    [0.6, 0x5362DA],
    [0.5, 0x646ED9],
    [0.4, 0x767BD8],
    [0.3, 0x8788D7],
    [0.2, 0x9894D6],
    [0.1, 0xA8A0D5],
    [0.0, 0xBAADD3],
    [-0.1, 0xCBB9D2],
    [-0.2, 0xD6C1CF],
    [-0.3, 0xD0BBC5],
    [-0.4, 0xCBB6BC],
    [-0.5, 0xC5B0B2],
    [-0.6, 0xBFAAA8],
    [-0.7, 0xBAA49E],
    [-0.8, 0xB49E95],
    [-0.9, 0xAF998C],
    [-1, 0x000000]
];

const viz = new ColorRampVisualizer(moistureRamps);

function evaluatePixel(samples) {
    // Calculate NDMI
    let ndmi = index(samples.B08, samples.B11);
    let imgVals = viz.process(ndmi);
    return imgVals.concat([samples.dataMask]);
}


    """
  else:
    return "Invalid filter"  

#################################################################################
""" @api_view(['POST'])
@csrf_exempt
def generate_raster_image(request):
    if request.method == "POST":
        min_x = float('inf')
        max_x = float('-inf')
        min_y = float('inf')
        max_y = float('-inf')
        coordinates = []
        coordinates_api = []
        #data = JSONParser().parse(request)
        #print(data)
        data = request.data
        date = data["date"]
        
        points = data["points"]
        
        for p in points:
            lang = float(p["fields"]["long"])
            latt = float(p["fields"]["latt"])
            coordinates.append([lang,latt])
        
        #print(coordinates)
        #for sublist in coordinates:
            #for pair in sublist:
            for pair in coordinates:
                if pair not in coordinates_api:
                    coordinates_api.append(pair)
                y, x = pair
                # Update the minimum and maximum x values if necessary
                if y < min_y:
                    min_y = y
                if y > max_y:
                    max_y = y
                # Update the minimum and maximum y values if necessary
                if x < min_x:
                    min_x = x
                if x > max_x:
                    max_x = x
        print(coordinates)
        coordinates_api.append(coordinates_api[0])
        print(coordinates_api)
        #print(min_x)
        #print(min_y)
        #print(max_x)
        #print(max_y) 
        search_data = {
                        "fields": [
                            "sceneID",
                            "cloudCoverage"
                        ],
                        "page": 1,
                        "search": {
                            "date": {
                                "from": date
                            },
                            "cloudCoverage": {
                                "from": 0,
                                "to": 80
                            },
                            "shape": {
                                "type": "Polygon",
                                "coordinates": [coordinates_api]
                            }
                        },
                        "sort": {
                            "date": "asc"
                        }
                        }
        #print(search_data)
        cropper_data = {
                        "type": "Feature",
                        "properties": {},
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [coordinates_api]
                        }
                        }
        #print(cropper_data)
        search_url_post = "https://gate.eos.com/api/lms/search/v2/sentinel2?api_key=apk.e082b3cf24cb3231d18cd3cf7751f21fccb56092d089447939f66530a0a0d211"
        search_post_response = requests.post(search_url_post, json=search_data)
        search_post_response_json = search_post_response.json()
        #print(search_post_response_json)
        search_results = search_post_response_json["results"]
        first_result = search_results[0]
        view_id = first_result["view_id"]
        print(view_id)
        cropper_url_post = "https://gate.eos.com/api/render/cropper/?api_key=apk.e082b3cf24cb3231d18cd3cf7751f21fccb56092d089447939f66530a0a0d211"
        cropper_post_response = requests.post(cropper_url_post, json=cropper_data)
        cropper_post_response_json = cropper_post_response.json()
        #print(cropper_post_response_json)
        cropper = cropper_post_response_json["cropper_ref"]
        print(cropper)
        filtre_value = data.get("filtre")
        #print(ndvi_value)
        raster_image_url = "https://gate.eos.com/api/render/{view_id}/{filtre}/10/{min_y};{max_y};4326/{min_x};{max_x};4326?cropper_ref={cropper}&CALIBRATE=1&COLORMAP=b4ba30aea7a40841c6f73a5bca2eca57&MIN_MAX=-1,1&MASKING=CLOUD&MASK_COLOR=fefefe&api_key=apk.e082b3cf24cb3231d18cd3cf7751f21fccb56092d089447939f66530a0a0d211".format(
            view_id=view_id,
            filtre=filtre_value,
            min_y=min_y,
            max_y=max_y,
            min_x=min_x,
            max_x=max_x,
            cropper=cropper
        )
        print(raster_image_url)
        return JsonResponse({"raster_image_url": raster_image_url, "min_y": min_y, "max_y": max_y, "min_x": min_x, "max_x": max_x}, status=status.HTTP_200_OK)
        #return JsonResponse(raster_image_url, status=status.HTTP_200_OK, safe=False)
        #return JsonResponse({"msg": "test en cours"}, status=status.HTTP_200_OK, safe=False) """


def about (request): 
    return render(request, 'about.html')
def accordion (request): 
    return render(request, 'accordion.html')
def alerts (request): 
    return render(request, 'alerts.html')
def avatar (request): 
    return render(request, 'avatar.html')
def background (request): 
    return render(request, 'background.html')
def badge (request): 
    return render(request, 'badge.html')
def blog_details (request): 
    return render(request, 'blog-details.html')
def blog_edit (request): 
    return render(request, 'blog-edit.html')
def blog (request): 
    return render(request, 'blog.html')
def border (request): 
    return render(request, 'border.html')
def breadcrumbs (request): 
    return render(request, 'breadcrumbs.html')
def buttons (request): 
    return render(request, 'buttons.html')
def calendar2 (request): 
    return render(request, 'calendar2.html')
def cards (request): 
    return render(request, 'cards.html')
def carousel (request): 
    return render(request, 'carousel.html')
def cart (request): 
    return render(request, 'cart.html')
def chart_chartjs (request): 
    return render(request, 'chart-chartjs.html')
def chart_echart (request):
    cookie = request.COOKIES.get('jwtToken')
    if cookie:
        user_group = request.COOKIES.get('userGroup') or None
        context = {
            'jwtToken': cookie,
            'userGroup': user_group,
        }
        print(context)
        return render(request, 'chart-echart.html', context)
    else: 
        return render(request, 'signin.html')
    
def chart_flot (request):
    cookie = request.COOKIES.get('jwtToken')
    if cookie:
        user_group = request.COOKIES.get('userGroup') or None
        context = {
            'jwtToken': cookie,
            'userGroup': user_group,
        }
        print(context)
        return render(request, 'chart-flot.html', context)
    else: 
        return render(request, 'signin.html')
     
def chart_morris (request): 
    return render(request, 'chart-morris.html')
def chart_nvd3 (request): 
    return render(request, 'chart-nvd3.html')
def chat (request): 
    return render(request, 'chat.html')
def checkout (request): 
    return render(request, 'checkout.html')
def client_create (request): 
    return render(request, 'client-create.html')
def clients (request): 
    return render(request, 'clients.html')
def colors (request): 
    return render(request, 'colors.html')
def construction (request): 
    return render(request, 'construction.html')
def counters (request): 
    return render(request, 'counters.html')
def datatable (request): 
    return render(request, 'datatable.html')
def display (request): 
    return render(request, 'display.html')
def dropdown (request): 
    return render(request, 'dropdown.html')
def empty (request): 
    return render(request, 'empty.html')
def error400 (request): 
    return render(request, 'error400.html')
def error404 (request): 
    return render(request, 'error404.html')
def error500 (request): 
    return render(request, 'error500.html')
def error501 (request): 
    return render(request, 'error501.html')
def faq (request): 
    return render(request, 'faq.html')
def file_attachments (request): 
    return render(request, 'file-attachments.html')
def file_manager_1 (request): 
    return render(request, 'file-manager-1.html')
def file_manager_2 (request): 
    return render(request, 'file-manager-2.html')
def file_manager (request): 
    return render(request, 'file-manager.html')
def flex (request): 
    return render(request, 'flex.html')
def footers (request): 
    return render(request, 'footers.html')
def forgot_password (request): 
    return render(request, 'forgot-password.html')
def form_advanced (request): 
    return render(request, 'form-advanced.html')
def form_editable (request): 
    return render(request, 'form-editable.html')
def form_elements (request): 
    return render(request, 'form-elements.html')
def form_layouts (request): 
    return render(request, 'form-layouts.html')
def form_validation (request): 
    return render(request, 'form-validation.html')
def form_wizard (request):
    cookie = request.COOKIES.get('jwtToken')
    if cookie:
        user_group = request.COOKIES.get('userGroup') or None
        context = {
            'jwtToken': cookie,
            'userGroup': user_group,
        }
        print(context)
        return render(request, 'form-wizard.html', context)
    else: 
        return render(request, 'signin.html') 
def gallery (request): 
    return render(request, 'gallery.html')
def height (request): 
    return render(request, 'height.html')
def icons (request): 
    return render(request, 'icons.html')
def icons2 (request): 
    return render(request, 'icons2.html')
def icons3 (request): 
    return render(request, 'icons3.html')
def icons4 (request): 
    return render(request, 'icons4.html')
def icons5 (request): 
    return render(request, 'icons5.html')
def icons6 (request): 
    return render(request, 'icons6.html')
def icons7 (request): 
    return render(request, 'icons7.html')
def icons8 (request): 
    return render(request, 'icons8.html')
def icons9 (request): 
    return render(request, 'icons9.html')
def icons10 (request): 
    return render(request, 'icons10.html')
""" def index (request):
    cookie = request.COOKIES.get('jwtToken')
    context = {'jwtToken': cookie} 
    print(context)
    return render(request, 'index.html') """
def invoice_create (request): 
    return render(request, 'invoice-create.html')
def invoice_details (request): 
    return render(request, 'invoice-details.html')
def invoice_edit (request): 
    return render(request, 'invoice-edit.html')
def invoice_list (request): 
    return render(request, 'invoice-list.html')
def invoice_timelog (request): 
    return render(request, 'invoice-timelog.html')
def landing (request): 
    return render(request, 'landing.html')
def loaders (request): 
    return render(request, 'loaders.html')
def lockscreen (request): 
    return render(request, 'lockscreen.html')

def abouthome (request): 
    return render(request, 'abouthome.html')

def home (request): 
    return render(request, 'home.html')

def signin (request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                
                serializer = CustomTokenObtainPairSerializer(data={'username': username, 'password': password})
                serializer.is_valid(raise_exception=True)
                token_data = serializer.validated_data            
                # Récupérez le groupe d'utilisateur et les permissions
                group = token_data['group']
                permissions = token_data['permissions']
                 
                # Générez le token de rafraîchissement
                refresh = RefreshToken.for_user(user)
                refresh_token = str(refresh)                               
                
                # Stockage du token dans les cookies
                response = redirect('index')
                response.set_cookie('jwtToken', token_data['access'], httponly=True)
                print(token_data)  
                response.set_cookie('refreshToken', refresh_token, httponly=True)
                response.set_cookie('userId', user.id)
                response.set_cookie('userGroup', group)
                response.set_cookie('userPermissions', ','.join(permissions))
                return response                                              
            else:
                messages.error(request, 'You have not confirmed your email. Please confirm it to activate your account.')
                return JsonResponse({'error': 'Email not confirmed'}, status=400)
        else:
            messages.error(request, 'Bad authentication')
            return render(request, 'error400.html',{'error': 'Authentication failed'}, status=400)
    return render(request, 'signin.html') 

def generate_jwt_token(user, group, permissions):
    secret_key = '43a4456d1b67fa78bccda3c21766fb2cadcb996f5db95487'
    expiration_time = datetime.utcnow() + timedelta(seconds=3600) 
   
    # Payload du token
    payload = {
        'token_type': 'access',
        'exp': expiration_time,
        'iat': datetime.utcnow(),
        'jti': str(uuid.uuid4()),
        'user_id': user.id,
        'username': user.username,
    }
    
    # Ajoutez le groupe au payload s'il est présent
    if group:
        payload['group'] = group.name
        print(group)

    # Ajoutez les permissions au payload s'il y en a
    if permissions:
        payload['permissions'] = list(permissions)
        print(permissions)

    # Génération du token
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    
    # Messages de débogage
    print("Generated Token:")
    print(token)
    print("Payload:")
    print(payload)
   
    return token 

def mail_compose (request): 
    return render(request, 'mail-compose.html')
def mail_inbox (request): 
    return render(request, 'mail-inbox.html')
def mail_read (request): 
    return render(request, 'mail-read.html')
def mail_settings (request): 
    return render(request, 'mail-settings.html')
def maps (request): 
    return render(request, 'maps.html')
def maps1 (request): 
    return render(request, 'maps1.html')
def maps2 (request): 
    return render(request, 'maps2.html')
def margin (request): 
    return render(request, 'margin.html')
def mediaobject (request): 
    return render(request, 'mediaobject.html')
def modal (request): 
    return render(request, 'modal.html')
def navigation (request): 
    return render(request, 'navigation.html')
def notify (request): 
    return render(request, 'notify.html')
def offcanvas (request): 
    return render(request, 'offcanvas.html')
def opacity (request): 
    return render(request, 'opacity.html')
def padding (request): 
    return render(request, 'padding.html')
def pagination (request): 
    return render(request, 'pagination.html')
def panels (request): 
    return render(request, 'panels.html')
def position (request): 
    return render(request, 'position.html')
def pricing (request): 
    return render(request, 'pricing.html')
def product_details (request):
    cookie = request.COOKIES.get('jwtToken')
    if cookie:
        user_group = request.COOKIES.get('userGroup') or None
        context = {
            'jwtToken': cookie,
            'userGroup': user_group,
        }
        print(context)
        return render(request, 'product-details.html', context)
    else: 
        return render(request, 'signin.html') 
  
def profile_user (request):
    cookie = request.COOKIES.get('jwtToken')
    if cookie:
        user_group = request.COOKIES.get('userGroup') or None
        try:
            profile = request.user.profile
            profile_company = request.user.profilecompany
        except ObjectDoesNotExist:
            profile = None
            profile_company = None
        context = {
            'jwtToken': cookie,
            'userGroup': user_group,
            'profile_user': profile,
            'profile_company': profile_company
        }                   
        print(context)
        return render(request, 'profile-user.html', context)
    else: 
        return render(request, 'signin.html') 

@login_required
def edit_profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile-user')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'edit-profile.html', {'form': form}) 

@login_required
def update_profile_image(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)

    if request.method == 'POST':
        form = ProfileImageForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile-user')
    else:
        form = ProfileImageForm(instance=profile)
        return render(request, 'profile-user.html', {'form': form})

def profile_update(request):
    if request.method == 'POST':
        user = request.user
        profile, created = Profile.objects.get_or_create(user=user)
        user.first_name = request.POST.get('first_name') if request.POST.get('first_name') else '' 
        user.last_name = request.POST.get('last_name') if request.POST.get('first_name') else ''
        user.save()
        
        
        if 'designation' in request.POST:
            profile.designation = request.POST['designation']
        if 'email' in request.POST:
            profile.email = request.POST['email']
        if 'website' in request.POST:
            profile.website = request.POST['website']
        if 'phone' in request.POST:
            profile.phone = request.POST['phone']
        if 'address' in request.POST:
            profile.address = request.POST['address']
            
        profile.save() 
        
        return redirect('profile-user')  
    else:
        return render(request, 'profile-user.html', {'user': request.user})
    
@login_required
def update_company_info(request):
    if request.method == 'POST':
        user = request.user
        profilecompany, created = ProfileCompany.objects.get_or_create(user=user)
        
        profilecompany.companyname = request.POST.get('companyname', '')
        profilecompany.activity = request.POST.get('activity', '')
        profilecompany.matricule = request.POST.get('matricule', '')
        profilecompany.address_company = request.POST.get('address_company', '')
        profilecompany.country = request.POST.get('country', '')
        profilecompany.website_company = request.POST.get('website_company', '')
        profilecompany.phoneNumber = request.POST.get('phoneNumber', '')
        profilecompany.area = request.POST.get('area', '')
        profilecompany.type_of_agriculture = request.POST.get('type_of_agriculture', '')

        logo_file = request.FILES.get('logo')
        if logo_file and isinstance(logo_file, InMemoryUploadedFile):
            profilecompany.logo = logo_file
        
        profilecompany.save() 
        
        return redirect('profile-user')  
    else:
        return render(request, 'profile-user.html', {'user': request.user})


##############################

def products (request): 
    return render(request, 'products.html')
def profile (request): 
    return render(request, 'profile.html')
def progress (request): 
    return render(request, 'progress.html')

def project_details (request, id):
    #print(id)
    zone = Zone.objects.get(pk=id)
    zone_serializer = ZoneSerializer(zone)
    map_form_data = serialize("json", MapForm.objects.all().filter(geozone=id))
    points = serialize("json", Point.objects.all().filter(geozone=id))
    zones_parcelles = ZoneParcelle.objects.all().filter(id_projet=id)
    parcelles = []
    for zp in zones_parcelles:
        map_form_parcelle = MapFormParcelle.objects.filter(geozone=zp).first()
        if map_form_parcelle:
            parcelles.append({
                'geozone_id': zp.pk,
                'parcelle_name': map_form_parcelle.parcelle_name
            })
    #print(zones_parcelles)
    points_parcelles_map = []
    for zp in zones_parcelles:
        points_zp = serialize("json", PointParcelle.objects.all().filter(geozone_id=zp.pk))
        points_parcelles_map.append(points_zp)
    print(points_parcelles_map)    
    z = zone_serializer.data
    #print(points)
    tp =  z["type"]
    #print(tp)
    radius = z["circle_radius"]
    #print(radius)
    cont = {
        'form': map_form_data
    }
    if tp == "circle":
            context = {
        'type': tp,
        'radius': radius,
        'points': points,
        }
            
    if tp == "polygon" or tp == "rectangle":
            context = {
        'type': tp,
        'points': points,
        }
    if tp == "polyline":
            context = {
        'type': tp,
        'points': points,
        }
    if tp == "marker":
            context = {
        'type': tp,
        'points': points,
        }
    form_data = json.dumps(cont, indent=4, sort_keys=True, default=str)
    map_points = json.dumps(context, indent=4, sort_keys=True, default=str)
    filters= serialize("json",Filtre.objects.all())
    print(filters)
    colors=  serialize("json",ColorReference.objects.all())
    print(colors)
    context = {
    'filters': filters,
    'colors': colors,
    }
    filters_colors = json.dumps(context, indent=4, sort_keys=True, default=str)
    data = {
        'points': map_points,
        'form': form_data,
        'points_parcelles_map': points_parcelles_map,
        'filters_colors': filters_colors
    }
    dumped_data = json.dumps(data, indent=4, sort_keys=True, default=str)
    return render(request, 'project-details.html', {'data': dumped_data,'project': {'parcelles': parcelles},})

def project_edit (request): 
    return render(request, 'project-edit.html')

@login_required
def project_new (request):
    cookie = request.COOKIES.get('jwtToken')
    if cookie:
        user_group = request.COOKIES.get('userGroup') or None
        try:
            profile = request.user.profile
        except objectDoesNotExist:
            profile = None
        context = {
            'jwtToken': cookie,
            'userGroup': user_group,
            'profile_user': profile,
            'projects': list  # Ajoutez la liste des projets à votre contexte
        }
        print(context)
        return render(request, 'project-new.html', context)
    else:
        # Si le jeton n'est pas présent, redirigez vers la page de connexion
        return render(request, 'signin.html') 

def project_new_form (request):  
    return render(request, 'project-new-form.html')

def projects_list (request):
    cookie = request.COOKIES.get('jwtToken')
    try:
        profile = request.user.profile
    except objectDoesNotExist:
        profile = None
    if cookie:
        user_group = request.COOKIES.get('userGroup') or None
        context = {
            'jwtToken': cookie,
            'userGroup': user_group,
            'profile_user': profile,
            'projects': list  # Ajoutez la liste des projets à votre contexte
        }
        print(context)
        return render(request, 'projects-list.html', context)
    else:
        # Si le jeton n'est pas présent, redirigez vers la page de connexion
        return render(request, 'signin.html') 

def projects (request): 
    list = []
    projects = reversed(MapForm.objects.all())
    for p in projects:
        project_id = p.__dict__["geozone_id"]
        parcelles =  MapFormParcelle.objects.all().filter(id_projet=project_id)
        print(parcelles)
        list.append({"project": p.__dict__, "parcelles": parcelles})
    data = {
        "list": list
    }
    dumped_data = json.dumps(data, indent=4, sort_keys=True, default=str)
    cookie = request.COOKIES.get('jwtToken')
    if cookie:
        user_group = request.COOKIES.get('userGroup') or None
        context = {
            'jwtToken': cookie,
            'userGroup': user_group,
            'projects': list  # Ajoutez la liste des projets à votre contexte
        }
        print(context)
        return render(request, 'projects.html', context)
    else:
        # Si le jeton n'est pas présent, redirigez vers la page de connexion
        return render(request, 'signin.html')

def parcelles(request):
    # Récupérer la liste des parcelles
    parcelles = reversed(MapFormParcelle.objects.all())
    print(parcelles)

    # Vérifier la présence du jeton JWT
    cookie = request.COOKIES.get('jwtToken')
    if cookie:
        user_group = request.COOKIES.get('userGroup') or None
        context = {
            'jwtToken': cookie,
            'userGroup': user_group,
            'parcelles': parcelles  # Ajouter la liste des parcelles au contexte
        }
        print(context)
        return render(request, 'parcelles.html', context)
    else:
        # Si le jeton n'est pas présent, rediriger vers la page de connexion
        return render(request, 'signin.html')

def parcelle_new (request):
    cookie = request.COOKIES.get('jwtToken')
    if cookie:
        user_group = request.COOKIES.get('userGroup') or None
        context = {
            'jwtToken': cookie,
            'userGroup': user_group,
            'parcelles': list  # Ajoutez la liste des projets à votre contexte
        }
        print(context)
        return render(request, 'parcelle-new.html', context)
    else:
        # Si le jeton n'est pas présent, redirigez vers la page de connexion
        return render(request, 'signin.html')
     
def parcelle_new_for_project(request, id):
    return render(request, 'parcelle-new.html', {'id_projet': id})
def parcelle_new_form (request): 
    return render(request, 'parcelle-new-form.html')
def parcelle_details (request, id):
    print(id)
    zone_parcelle = ZoneParcelle.objects.get(pk=id) 
    zone_parcelle_serializer = ZoneParcelleSerializer(zone_parcelle)
    map_form_parcelle_data = serialize("json", MapFormParcelle.objects.all().filter(geozone=id))
    points = serialize("json", PointParcelle.objects.all().filter(geozone=id))
    z = zone_parcelle_serializer.data
    print(points)
    tp =  z["type"]
    print(tp)
    radius = z["circle_radius"]
    print(radius)
    cont = {
        'form': map_form_parcelle_data
    }
    if tp == "circle":
            context = {
        'type': tp,
        'radius': radius,
        'points': points,
        }
            
    if tp == "polygon" or tp == "rectangle":
            context = {
        'type': tp,
        'points': points,
        }
    if tp == "polyline":
            context = {
        'type': tp,
        'points': points,
        }
    if tp == "marker":
            context = {
        'type': tp,
        'points': points,
        }
    form_data = json.dumps(cont, indent=4, sort_keys=True, default=str)
    map_points = json.dumps(context, indent=4, sort_keys=True, default=str)
    filters= serialize("json",Filtre.objects.all())
    print(filters)
    colors=  serialize("json",ColorReference.objects.all())
    print(colors)
    context = {
    'filters': filters,
    'colors': colors,
    }
    filters_colors = json.dumps(context, indent=4, sort_keys=True, default=str)
    data = {
        'points': map_points,
        'form': form_data,
        'filters_colors': filters_colors
    }
    dumped_data = json.dumps(data, indent=4, sort_keys=True, default=str)
    return render(request, 'parcelle-details.html', {'data': dumped_data})

def parcelles_list (request): 
    return render(request, 'parcelles-list.html')
def parcelle_edit (request): 
    return render(request, 'parcelle-edit.html')
def rangeslider (request): 
    return render(request, 'rangeslider.html')
def rating (request): 
    return render(request, 'rating.html')

def register1 (request): 
    return render(request, 'register1.html')
#@api_view(['POST'])
@csrf_exempt
def register (request): 
    if request.method == "POST":
        username = request.POST['username']
        print(username)
        firstname = request.POST['firstname']
        print(firstname)
        lastname = request.POST['lastname']
        print(lastname)
        email = request.POST['email']
        print(email)
        password = request.POST['password']
        print(password)
        confirmpassword = request.POST['confirmpwd']
        print(confirmpassword)
        selected_group_id = request.POST['group']
        selected_group = selected_group_id
        print(selected_group_id)
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'username already taken please try another.')
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'This email has an account.')
            return redirect('register')  
        if len(username) > 10 or len(username) < 5 or not username.isalnum():
            messages.error(request, 'Invalid username. It must be between 5 and 10 alphanumeric characters.')
            return redirect('register') 

        if password != confirmpassword:
            messages.error(request, 'The password did not match! ')  
            return redirect('register')                  

        my_user = User.objects.create_user(username, email, password)
        my_user.first_name =firstname
        my_user.last_name = lastname
        my_user.is_active = False
        my_user.save()
        if selected_group:
            group = Group.objects.get(name=selected_group)
            my_user.groups.add(group)
        form = {
                "username": username,
                "firstname": firstname,
                "lastname": lastname,
                "email": email,
                "password": password,
                "confirmpwd": confirmpassword,
                "group": selected_group
        } 
               
        messages.success(request, 'Your account has been successfully created. we have sent you an email You must comfirm in order to activate your account.')
# send email when account has been created successfully
        subject = "Welcome to Magon-application SSS"
        message = "Welcome "+ my_user.first_name + " " + my_user.last_name + "\n thank for chosing Magon.\n To order login you need to comfirm your email account.\n thanks\n\n\n SSS"
        
        from_email = conf_settings.EMAIL_HOST_USER
        to_list = [my_user.email]
        send_mail(subject, message, from_email, to_list, fail_silently=False)

# send the the confirmation email
        current_site = get_current_site(request) 
        email_suject = "confirm your email SSS Magon Login!"
        messageConfirm = render_to_string("emailConfirmation.html", {
            'name': my_user.first_name,
            'domain':current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(my_user.pk)),
            'token': default_token_generator.make_token(my_user)
        })       

        email = EmailMessage(
            email_suject,
            messageConfirm,
            conf_settings.EMAIL_HOST_USER,
            [my_user.email]
        )

        email.fail_silently = False
        email.send() 
        return redirect('signin') 
    return render(request, 'register.html')
    
def scroll (request): 
    return render(request, 'scroll.html')
def services (request): 
    return render(request, 'services.html')
def settings (request): 
    return render(request, 'settings.html')
def sweetalert (request): 
    return render(request, 'sweetalert.html')
def switcherpage (request): 
    return render(request, 'switcherpage.html')
def table_editable (request): 
    return render(request, 'table-editable.html')
def tables (request): 
    return render(request, 'tables.html')
def tabs (request): 
    return render(request, 'tabs.html')
def tags (request): 
    return render(request, 'tags.html')
def task_create (request): 
    return render(request, 'task-create.html')
def task_edit (request): 
    return render(request, 'task-edit.html')
def tasks_list (request): 
    return render(request, 'tasks-list.html')
def terms (request): 
    return render(request, 'terms.html')
def thumbnails (request): 
    return render(request, 'thumbnails.html')
def ticket_details (request): 
    return render(request, 'ticket-details.html')
def timeline (request): 
    return render(request, 'timeline.html')
def tooltipandpopover (request): 
    return render(request, 'tooltipandpopover.html')
def treeview (request): 
    return render(request, 'treeview.html')
def typography (request): 
    return render(request, 'typography.html')
def users_list (request): 
    return render(request, 'users-list.html')
def width (request): 
    return render(request, 'width.html')
def wishlist (request): 
    return render(request, 'wishlist.html')
def wysiwyag (request): 
    return render(request, 'wysiwyag.html')

""" def check_logistiques_access(request):
    permissions_list = list(request.user.get_all_permissions())    
    return JsonResponse({'permissions': permissions_list}) """
    
def check_logistiques_access(request):
    permissions_list = list(request.user.get_all_permissions())    
    return {'permissions': permissions_list}

def logistiques(request):
    print(request.user)
    access_response = check_logistiques_access(request)
    print(access_response)

    cookie = request.COOKIES.get('jwtToken')
    if cookie:
        user_group = request.COOKIES.get('userGroup') or None
        context = {
            'jwtToken': cookie,
            'userGroup': user_group,
        }

        if 'permissions' in access_response:
            has_permission = 'app.view_logistiques' in access_response['permissions']

            if has_permission:
                return render(request, 'logistiques.html', context)
            else:
                alert_message = 'Accès refusé. Vous n\'avez pas la permission.'
                return render(request, 'popup.html', {'alert_message': alert_message, 'redirect_url': 'index'})
        else:
            return render(request, 'popup.html', {'alert_message': 'Erreur: Clé "permissions" manquante dans la réponse.', 'redirect_url': 'index'})
    else:
        return render(request, 'signin.html')

def logistiques_list (request):
    return render(request, 'logistiques-list.html')

def popup_view(request):
    return render(request, 'popup_template.html')
""" def popup (request):
    return render(request, 'popup.html') """

def machines_engins (request):
    list = []
    machines = Machines_Tables.objects.all()
    types_machines = TypeMachineEngins.objects.all()
    list.append({"types": types_machines,"machines": machines})
    """ user = request.user
    print(user)
    groups = user.groups.filter(name='regular')
    print(groups)
    if groups.exists(): """
    return render(request, 'machines-engins.html', {'data': list})
    """ else:
        return redirect('permission_denied') """

def outils_agricoles (request):
    list = []
    outils = Outils_Tables.objects.all()
    types_outils = TypeOutilsAgricoles.objects.all()
    list.append({"types": types_outils,"outils": outils})
    return render(request, 'outils-agricoles.html', {'data': list})

def infrastructure (request):
    return render(request, 'infrastructure.html')
def fertilisants_traitements (request):
    return render(request, 'fertilisants-traitements.html')

def graines_pousses (request):
    list = []
    graines = Graine_Tables.objects.all()
    types_graines = TypeGrainesPousses.objects.all()
    categories_graines = CategorieGrainesPousses.objects.all()
    projects = MapForm.objects.all()
    list.append({"types": types_graines,"categories": categories_graines, "graines":graines, "projects": projects})
    return render(request, 'graines-pousses.html', {'data': list})

def carburant (request):
    list = []
    carburants = Carburants_Tables.objects.all()
    types_carburants = TypeCarburant.objects.all()
    list.append({"types": types_carburants,"carburants": carburants})
    return render(request, 'carburant.html', {'data': list})

def rh (request):
    list = []
    rhs = Rh_Tables.objects.all()
    types_rhs = TypeRh.objects.all()
    projects = MapForm.objects.all()
    list.append({"types": types_rhs,"rhs": rhs, "projects": projects})
    return render(request, 'rh.html', {'data': list})

def pieces_rechange (request):
    list = []
    pieces = Pieces_Tables.objects.all()
    types_pieces = TypePieces.objects.all()
    list.append({"types": types_pieces,"pieces": pieces})
    return render(request, 'pieces-rechange.html', {'data': list})

def reseaux_irrigation (request):
    return render(request, 'reseaux-irrigation.html')
def reseaux_electrique (request):
    return render(request, 'reseaux-electrique.html')

def poste_transformateur (request):
    return render(request, 'poste-transformateur.html')
def panneaux_pv (request):
    return render(request, 'panneaux-pv.html')
def generatur (request):
    return render(request, 'generatur.html')

def moteur (request):
    list = []
    #moteurs = Moteur_Tables.objects.all()
    type_moteur = TypeMoteur.objects.all()
    type_tension = TypeTensionMoteur.objects.all()
    print(type_tension)
    type_couplage = TypeCouplageMoteur.objects.all()
    projects = MapForm.objects.all()
    list.append({"types": type_moteur,"tensions": type_tension,"couplages": type_couplage,"projects": projects})
    return render(request, 'moteur.html', {'data': list})

def securite (request):
    return render(request, 'securite.html')
def batiments (request):
    return render(request, 'batiments.html')

def maison_villa (request):
    list = []
    maisons = Maison_Tables.objects.all()
    types_maisons = TypeMaisonVilla.objects.all()
    projects = MapForm.objects.all()
    list.append({"types": types_maisons,"maisons": maisons, "projects": projects})
    return render(request, 'maison-villa.html', {'data': list})

def hangar_depot (request):
    list = []
    hangars = Hangar_Tables.objects.all()
    types_hangars = TypeHangerDepot.objects.all()
    projects = MapForm.objects.all()
    list.append({"types": types_hangars,"hangars": hangars, "projects": projects})
    return render(request, 'hangar-depot.html', {'data': list})

def local_technique (request):
    list = []
    """ locals = Local_Tables.objects.all()
    types_locals = TypeLocal.objects.all() """
    projects = MapForm.objects.all()
    #list.append({"types": types_locals,"locals": locals, "projects": projects})
    return render(request, 'local-technique.html', {'data': list})

def frigo (request):
    return render(request, 'frigo.html')

def engrais (request):
    list = []
    engrais = Engrais_Tables.objects.all()
    types_engrais = TypeEngrais.objects.all()
    categories_Engrais = CategorieEngrais.objects.all()
    projects = MapForm.objects.all()
    list.append({"types": types_engrais,"categories": categories_Engrais, "engrais":engrais, "projects": projects})
    return render(request, 'engrais.html', {'data': list})



def autres (request):
    return render(request, 'autres.html')

def machines_engins_new (request):
    return render(request, 'machines-engins-new.html')

def operations_utilisateur (request):
    cookie = request.COOKIES.get('jwtToken')
    if cookie:
        user_group = request.COOKIES.get('userGroup') or None
        context = {
            'jwtToken': cookie,
            'userGroup': user_group,
        }
        print(context)
        return render(request, 'operations-utilisateur.html', context)
    else:
        return render(request, 'signin.html')

def recommendations_ia (request):
    cookie = request.COOKIES.get('jwtToken')
    if cookie:
        user_group = request.COOKIES.get('userGroup') or None
        context = {
            'jwtToken': cookie,
            'userGroup': user_group,
        }
        print(context)
        return render(request, 'recommendations-ia.html', context)
    else:
        return render(request, 'signin.html')

def ajouter_operation_agricole (request):
    cookie = request.COOKIES.get('jwtToken')
    if cookie:
        user_group = request.COOKIES.get('userGroup') or None
        context = {
            'jwtToken': cookie,
            'userGroup': user_group,
        }
        print(context)
        return render(request, 'ajouter-operation-agricole.html', context)
    else:
        return render(request, 'signin.html')
    
def puit (request): 
    return render(request, 'puit.html')

def reservoir (request): 
    return render(request, 'reservoir.html')

def vanne (request): 
    return render(request, 'vanne.html')

def goutte (request): 
    return render(request, 'goutte.html')

def pivot (request): 
    return render(request, 'pivot.html')

def pulverisateur (request): 
    return render(request, 'pulverisateur.html')

def meteo (request):
    return render(request, 'meteo.html')
class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['image']
        
def analyse (request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save()
            image_path = uploaded_image.image.path

            with open(image_path, 'rb') as image_file:
                files = {'file': image_file}

                # Remplacez 'NGROK_PUBLIC_URL' par l'URL réelle de votre service Ngrok
                ngrok_url = 'https://a058-35-237-126-147.ngrok-free.app/predict'
                response = requests.post(ngrok_url, files=files)

                if response.status_code == 200:
                    # Chemin complet pour sauvegarder l'image traitée
                    result_image_dir = 'D:/MAGON_3SSS/MAGON_3SSS/MAGON_3SSS-main/MAGON_3S/media/results/'
                    result_image_name = f'result_{uploaded_image.id}.png'
                    result_image_path = os.path.join(result_image_dir, result_image_name)

                    # Sauvegarde de l'image traitée
                    with open(result_image_path, 'wb') as f:
                        f.write(response.content)

                    # Mise à jour de l'objet UploadedImage pour pointer vers l'image traitée
                    uploaded_image.result_image.name = os.path.join('/results', result_image_name)
                    uploaded_image.save()
                    

                    return render(request, 'image_result.html', {'upload_image': uploaded_image})
                else:
                    return HttpResponse('Erreur lors du traitement de l\'image', status=500)
    else:
        form = ImageUploadForm() 
    return render(request, 'analyse.html', {'form': form})

def analyse_details (request):
    cookie = request.COOKIES.get('jwtToken')
    if cookie:
        user_group = request.COOKIES.get('userGroup') or None
        context = {
            'jwtToken': cookie,
            'userGroup': user_group,
        }
        print(context)
        return render(request, 'analyse-details.html', context)
    else: 
        return render(request, 'signin.html')