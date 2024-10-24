import difflib
from django.conf import settings as conf_settings
from django.conf import settings
import base64
import io
import mimetypes
from uuid import uuid4
import uuid
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.http import HttpResponse, HttpResponseServerError, JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.tokens import default_token_generator 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login , logout
from django.contrib import messages
from django.core.serializers import serialize
#from rest_framework import serializers
#from django.core import serializers as core_serializers
from rest_framework.authentication import SessionAuthentication
from django.core.mail import send_mail, EmailMessage
from numpy import DataSource
from app.authentication import get_user_permissions
from noa import settings

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from app.models import Hangar_Tables, TypeHangerDepot, Zone
from app.serializers import CustomTokenObtainPairSerializer, OperationsSerializer, ZoneSerializer
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
#from app.models import Filtre
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
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q

##############  ADMIN #####################
# Formulaire pour ajouter un nouvel utilisateur avec un groupe
class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, label="Groupe d'utilisateur")

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'group']

# Formulaire pour gérer les permissions d'un groupe
class GroupPermissionForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Permissions"
    )

    class Meta:
        model = Group
        fields = ['permissions']

# Formulaire pour modifier le groupe d'un utilisateur existant
class UserGroupForm(forms.ModelForm):
    groups = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, label="Groupe")

    class Meta:
        model = User
        fields = ['groups']
        
# Formulaire pour ajouter un nouveau groupe
class GroupCreationForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']
        labels = {'name': "Nom du groupe"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nom du Groupe'})

@login_required
def admin_dashboard(request):
    total_users = User.objects.count()

    # Initialisation des formulaires
    user_form = UserCreationForm()
    group_form = UserGroupForm()
    group_creation_form = GroupCreationForm()  # Nouveau formulaire pour créer un groupe

    if request.method == "POST":
        # Ajouter un nouvel utilisateur
        if 'add_user' in request.POST:
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.save()
                selected_group = form.cleaned_data['group']
                selected_group.user_set.add(user)
                messages.success(request, f"Utilisateur {user.username} ajouté avec succès au groupe {selected_group.name} !")
                return redirect('admin_dashboard')

        # Supprimer un utilisateur existant
        if 'delete_user' in request.POST:
            username_to_delete = request.POST.get('username_to_delete')
            try:
                user_to_delete = User.objects.get(username=username_to_delete)
                user_to_delete.delete()
                messages.success(request, 'Utilisateur supprimé avec succès !')
            except User.DoesNotExist:
                messages.error(request, 'Utilisateur non trouvé.')

        # Changer le groupe d'un utilisateur existant
        if 'change_group' in request.POST:
            username_to_update = request.POST.get('username_to_update')
            group_id = request.POST.get('group')
            try:
                user_to_update = User.objects.get(username=username_to_update)
                new_group = Group.objects.get(id=group_id)
                
                # Supprimer l'utilisateur de tous ses groupes actuels
                user_to_update.groups.clear()
                
                # Ajouter l'utilisateur au nouveau groupe
                user_to_update.groups.add(new_group)
                messages.success(request, f"Groupe de {user_to_update.username} mis à jour avec succès au groupe {new_group.name} !")
            except (User.DoesNotExist, Group.DoesNotExist):
                messages.error(request, 'Utilisateur ou groupe non trouvé.')

        # Ajouter un nouveau groupe
        if 'add_group' in request.POST:
            group_form = GroupCreationForm(request.POST)
            if group_form.is_valid():
                group_form.save()
                messages.success(request, 'Nouveau groupe ajouté avec succès !')
                return redirect('admin_dashboard')

    users = User.objects.all()
    groups = Group.objects.all()  # Récupérer tous les groupes

    context = {
        'total_users': total_users,
        'users': users,
        'groups': groups,
        'user_form': user_form,
        'group_form': group_form,
        'group_creation_form': group_creation_form,  # Formulaire pour créer un nouveau groupe
    }
    return render(request, 'admin_dashboard.html', context)

# Vue pour gérer les permissions des groupes
@login_required
def manage_groups_permissions(request):
    groups = Group.objects.all()
    
    if request.method == 'POST':
        for group in groups:
            form = GroupPermissionForm(request.POST, instance=group)
            if form.is_valid():
                form.save()
                messages.success(request, f"Permissions du groupe {group.name} mises à jour avec succès !")
        return redirect('manage_groups_permissions')

    # Créer un formulaire pour chaque groupe
    group_forms = {group.name: GroupPermissionForm(instance=group) for group in groups}

    context = {
        'groups': groups,
        'group_forms': group_forms,
    }
    return render(request, 'manage_groups_permissions.html', context)

class FiltreVegetationForm(forms.ModelForm):
    class Meta:
        model = FiltreVegitation
        fields = ['abreviation', 'descriptionFr', 'descriptionAr', 'details']

class FiltreHumiditeForm(forms.ModelForm):
    class Meta:
        model = FiltreHumidite
        fields = ['abreviation', 'descriptionFr', 'descriptionAr', 'details']

class FiltreIrrigationForm(forms.ModelForm):
    class Meta:
        model = FiltreIrrigation
        fields = ['abreviation', 'descriptionFr', 'descriptionAr', 'details']
        
class FiltreFertilisationForm(forms.ModelForm):
    class Meta:
        model = FiltreFertilisation
        fields = ['abreviation', 'descriptionFr', 'descriptionAr', 'details']
        
class FiltreEvolutionForm(forms.ModelForm):
    class Meta:
        model = FiltreEvolution
        fields = ['abreviation', 'descriptionFr', 'descriptionAr', 'details']
        
class FiltreMaladieForm(forms.ModelForm):
    class Meta:
        model = FiltreMaladie
        fields = ['abreviation', 'descriptionFr', 'descriptionAr', 'details']

# Vue pour gérer les filtres 
def admin_filtre_view(request):
    # Récupérer tous les filtres de chaque catégorie
    filtres_vegetation = FiltreVegitation.objects.all()
    filtres_humidite = FiltreHumidite.objects.all()
    filtres_irrigation = FiltreIrrigation.objects.all()
    filtres_fertilisation = FiltreFertilisation.objects.all()
    filtres_evolution = FiltreEvolution.objects.all()
    filtres_maladie = FiltreMaladie.objects.all()

    # Initialiser les formulaires pour chaque catégorie
    form_vegetation = FiltreVegetationForm(request.POST or None, prefix='vegetation')
    form_humidite = FiltreHumiditeForm(request.POST or None, prefix='humidite')
    form_irrigation = FiltreIrrigationForm(request.POST or None, prefix='irrigation')
    form_fertilisation = FiltreFertilisationForm(request.POST or None, prefix='fertilisation')
    form_evolution = FiltreEvolutionForm(request.POST or None, prefix='evolution')
    form_maladie = FiltreMaladieForm(request.POST or None, prefix='maladie')

    # Gérer l'ajout selon le formulaire envoyé
    if request.method == 'POST':
        if 'add_vegetation' in request.POST:
            # Vérifier la validité du formulaire de Végétation
            if form_vegetation.is_valid():
                form_vegetation.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'Form invalid'}, status=400)
                #return redirect('admin_filtre_view')

        elif 'add_humidite' in request.POST:
            if form_humidite.is_valid():
                form_humidite.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'Form invalid'}, status=400)
                #return redirect('admin_filtre_view')

        elif 'add_irrigation' in request.POST:
            if form_irrigation.is_valid():
                form_irrigation.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'Form invalid'}, status=400)
                #return redirect('admin_filtre_view')

        elif 'add_fertilisation' in request.POST:
            if form_fertilisation.is_valid():
                form_fertilisation.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'Form invalid'}, status=400)
                #return redirect('admin_filtre_view')

        elif 'add_evolution' in request.POST:
            if form_evolution.is_valid():
                form_evolution.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'Form invalid'}, status=400)
                #return redirect('admin_filtre_view')

        elif 'add_maladie' in request.POST:
            if form_maladie.is_valid():
                form_maladie.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'Form invalid'}, status=400)
                #return redirect('admin_filtre_view')

        return redirect('admin_filtre_view')

    return render(request, 'admin_filtre.html', {
        'filtres_vegetation': filtres_vegetation,
        'filtres_humidite': filtres_humidite,
        'filtres_irrigation': filtres_irrigation,
        'filtres_fertilisation': filtres_fertilisation,
        'filtres_evolution': filtres_evolution,
        'filtres_maladie': filtres_maladie,
        'form_vegetation': form_vegetation,
        'form_humidite': form_humidite,
        'form_irrigation': form_irrigation,
        'form_fertilisation': form_fertilisation,
        'form_evolution': form_evolution,
        'form_maladie': form_maladie,
    })

def edit_filtre_view(request):
    if request.method == 'POST':
        filter_type = request.POST.get('filter_type')
        filtre_id = request.POST.get('filter-id')
        
        # Debugging: Print the POST data
        print("Received POST data:", request.POST)
        
        if not filtre_id:
            return JsonResponse({'success': False, 'message': 'Filter ID is missing.'}, status=400)
        
        try:
            filtre_id = int(filtre_id)
        except ValueError:
            return JsonResponse({'success': False, 'message': 'Invalid Filter ID.'}, status=400)
        
        abreviation = request.POST.get('edit-abreviation')
        descriptionFr = request.POST.get('edit-descriptionFr')
        descriptionAr = request.POST.get('edit-descriptionAr')
        details = request.POST.get('edit-details')
        
        # Determine the correct model based on filter_type
        filter_models = {
            'vegetation': FiltreVegitation,
            'humidite': FiltreHumidite,
            'irrigation': FiltreIrrigation,
            'fertilisation': FiltreFertilisation,
            'evolution': FiltreEvolution,
            'maladie': FiltreMaladie,
        }
        
        Model = filter_models.get(filter_type)
        if not Model:
            return JsonResponse({'success': False, 'message': 'Unsupported filter type.'}, status=400)
        
        filtre = get_object_or_404(Model, id=filtre_id)
        
        # Update the filter fields
        filtre.abreviation = abreviation
        filtre.descriptionFr = descriptionFr
        filtre.descriptionAr = descriptionAr
        filtre.details = details
        filtre.save()
        
        messages.success(request, "Filtre modifié avec succès.")
        return JsonResponse({'success': True})
    
    return HttpResponseBadRequest("Invalid request")
    
def delete_filtre(request, id):
    if request.method == 'DELETE':
        #filtre = get_object_or_404(FiltreVegitation, id=id)
        # Détecter le type de filtre à partir du formulaire ou d'un paramètre
        filter_type = request.GET.get('filter_type')  # Utiliser un paramètre 'filter_type' dans l'URL

        if filter_type == 'vegetation':
            filtre = get_object_or_404(FiltreVegitation, id=id)
        elif filter_type == 'humidite':
            filtre = get_object_or_404(FiltreHumidite, id=id)
        elif filter_type == 'irrigation':
            filtre = get_object_or_404(FiltreIrrigation, id=id)
        elif filter_type == 'fertilisation':
            filtre = get_object_or_404(FiltreFertilisation, id=id)
        elif filter_type == 'evolution':
            filtre = get_object_or_404(FiltreEvolution, id=id)
        elif filter_type == 'maladie':
            filtre = get_object_or_404(FiltreMaladie, id=id)
        else:
            return HttpResponseBadRequest("Type de filtre non pris en charge")
        filtre.delete()
        return JsonResponse({'success': True})
    return HttpResponseBadRequest("Invalid request")
##############  ADMIN #####################

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

def moteur_list (request):
    list = []
    #moteurs = Moteur_Tables.objects.all()
    type_moteur = TypeMoteur.objects.all()
    type_tension = TypeTensionMoteur.objects.all()
    print(type_tension)
    type_couplage = TypeCouplageMoteur.objects.all()
    projects = MapForm.objects.all()
    list.append({"types": type_moteur,"tensions": type_tension,"couplages": type_couplage,"projects": projects})
    return render(request, 'moteur-list.html', {'data': list})

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
# List Engrais
def engrais (request):
    list = []
    engrais = Engrais_Tables.objects.filter(user=request.user)
    types_engrais = TypeEngrais.objects.all()
    categories_Engrais = CategorieEngrais.objects.all()
    projects = MapForm.objects.all()
    list.append({"types": types_engrais,"categories": categories_Engrais, "engrais":engrais, "projects": projects})
    return render(request, 'engrais.html', {'data': list})
# List Tableau Engrais
def engrais_list (request):
    list = []
    engrais = Engrais_Tables.objects.filter(user=request.user)
    types_engrais = TypeEngrais.objects.all()
    categories_Engrais = CategorieEngrais.objects.all()
    projects = MapForm.objects.all()
    list.append({"types": types_engrais,"categories": categories_Engrais, "engrais":engrais, "projects": projects})
    return render(request, 'engrais-list.html', {'data': list})
# Save Engrais
@api_view(['POST'])
@authentication_classes([SessionAuthentication])  
@permission_classes([IsAuthenticated])
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
                "description": description,
                "user": request.user.id
            }
        
        engrai_serializer = EngraisSerializer(data=form)
                
        if engrai_serializer.is_valid():
            print('yes')
            engrai_serializer.save()
            return JsonResponse(engrai_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('no')
            return JsonResponse({"Erreur": "Some error occured"}, status=status.HTTP_201_CREATED)
# Afficher Engrais       
def get_engrai(request, engrai_id):
    try:
        engrai = Engrais_Tables.objects.get(id=engrai_id)
        project = MapForm.objects.filter(geozone=engrai.geozone).first()
        data = {
            'id': engrai.id,
            'nom': engrai.nom,
            'type': engrai.type,
            'categorie': engrai.categorie,
            'composition': engrai.composition,
            'mode_utilisation': engrai.mode_utilisation,
            'dosage': engrai.dosage,
            'quantite': engrai.quantite,
            'date_achat': engrai.date_achat,
            'cout': engrai.cout,
            'geozone_name': project.project_name if project else 'No project found',  # Add project name
            'geozone_id': engrai.geozone.id if engrai.geozone else None,  # Add geozone ID
            'description': engrai.description,
            'image': engrai.image.url if engrai.image else '',
        }
        return JsonResponse(data, status=200)
    except Engrais_Tables.DoesNotExist:
        return JsonResponse({"error": "Engrais not found"}, status=404)
# Details Engrais   
def get_engrai_details(request, engrai_id):
    try:
        engrai = Engrais_Tables.objects.get(id=engrai_id)
        project = MapForm.objects.filter(geozone=engrai.geozone).first()
        data = {
            'id': engrai.id,
            'nom': engrai.nom,
            'type': engrai.type,
            'categorie': engrai.categorie,
            'composition': engrai.composition,
            'mode_utilisation': engrai.mode_utilisation,
            'dosage': engrai.dosage,
            'quantite': engrai.quantite,
            'date_achat': engrai.date_achat,
            'cout': engrai.cout,
            'geozone_name': project.project_name if project else 'No project found',  # Add project name
            'geozone_id': engrai.geozone.id if engrai.geozone else None,  # Add geozone ID
            'description': engrai.description,
            'image': engrai.image.url if engrai.image else '',
        }
        return JsonResponse(data, status=200)
    except Engrais_Tables.DoesNotExist:
        return JsonResponse({"error": "Engrais not found"}, status=404)
# Edit Engrais details
def edit_engrai(request, engrai_id):
    try:
        engrai = Engrais_Tables.objects.get(id=engrai_id)

        engrai.nom = request.POST.get('nom')
        engrai.type = request.POST.get('type_engrais')
        engrai.categorie = request.POST.get('categorie_engrais')
        engrai.composition = request.POST.get('composition')
        engrai.mode_utilisation = request.POST.get('mode_utilisation')
        engrai.dosage = request.POST.get('dosage')
        engrai.quantite = request.POST.get('quantite')
        engrai.date_achat = request.POST.get('date_achat')
        engrai.cout = request.POST.get('cout')
        engrai.description = request.POST.get('description')
        engrai.geozone_id = request.POST.get('geozone')

        if 'image' in request.FILES:
            engrai.image = request.FILES['image']

        engrai.save()

        return JsonResponse({"success": "Engrais updated successfully"}, status=200)
    except Engrais_Tables.DoesNotExist:
        return JsonResponse({"error": "Engrais not found"}, status=404)
# Delete Engrais
def delete_engrai(request, engrai_id):
    try:
        engrai = Engrais_Tables.objects.get(id=engrai_id)
        engrai.delete()
        return JsonResponse({"success": "Engrais deleted successfully"}, status=200)
    except Engrais_Tables.DoesNotExist:
        return JsonResponse({"error": "Engrais not found"}, status=404)

""" Traitements """
def traitements (request):
    list = []
    traitements = Traitement_Tables.objects.filter(user=request.user)
    types_traitements = TypeTraitement.objects.all()
    categories_Traitements = CategorieTraitement.objects.all()
    projects = MapForm.objects.all()
    list.append({"types": types_traitements,"categories": categories_Traitements, "traitements":traitements, "projects": projects})
    return render(request, 'traitements.html', {'data': list})

def traitements_list (request):
    list = []
    traitements = Traitement_Tables.objects.filter(user=request.user)
    types_traitements = TypeTraitement.objects.all()
    categories_Traitements = CategorieTraitement.objects.all()
    projects = MapForm.objects.all()
    list.append({"types": types_traitements,"categories": categories_Traitements, "traitements":traitements, "projects": projects})
    return render(request, 'traitements-list.html', {'data': list})

@api_view(['POST'])
@authentication_classes([SessionAuthentication])  
@permission_classes([IsAuthenticated])
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
# Afficher Traitement       
def get_traitement(request, traitement_id):
    try:
        traitement = Traitement_Tables.objects.get(id=traitement_id)
        project = MapForm.objects.filter(geozone=traitement.geozone).first()
        data = {
            'id': traitement.id,
            'nom': traitement.nom,
            'type': traitement.type,
            'categorie': traitement.categorie,
            'composition': traitement.composition,
            'mode_utilisation': traitement.mode_utilisation,
            'dosage': traitement.dosage,
            'quantite': traitement.quantite,
            'date_achat': traitement.date_achat,
            'cout': traitement.cout,
            'geozone_name': project.project_name if project else 'No project found',  # Add project name
            'geozone_id': traitement.geozone.id if traitement.geozone else None,  # Add geozone ID
            'description': traitement.description,
            'image': traitement.image.url if traitement.image else '',
        }
        return JsonResponse(data, status=200)
    except Traitement_Tables.DoesNotExist:
        return JsonResponse({"error": "Tratements not found"}, status=404)
# Details Traitement   
def get_traitement_details(request, traitement_id):
    try:
        traitement = Traitement_Tables.objects.get(id=traitement_id)
        project = MapForm.objects.filter(geozone=traitement.geozone).first()
        data = {
            'id': traitement.id,
            'nom': traitement.nom,
            'type': traitement.type,
            'categorie': traitement.categorie,
            'composition': traitement.composition,
            'mode_utilisation': traitement.mode_utilisation,
            'dosage': traitement.dosage,
            'quantite': traitement.quantite,
            'date_achat': traitement.date_achat,
            'cout': traitement.cout,
            'geozone_name': project.project_name if project else 'No project found',  # Add project name
            'geozone_id': traitement.geozone.id if traitement.geozone else None,  # Add geozone ID
            'description': traitement.description,
            'image': traitement.image.url if traitement.image else '',
        }
        return JsonResponse(data, status=200)
    except Traitement_Tables.DoesNotExist:
        return JsonResponse({"error": "Traitement not found"}, status=404)
# Edit Traitements details
def edit_traitement(request, traitement_id):
    try:
        traitement = Traitement_Tables.objects.get(id=traitement_id)

        traitement.nom = request.POST.get('nom')
        traitement.type = request.POST.get('type_traitement')
        traitement.categorie = request.POST.get('categorie_traitement')
        traitement.composition = request.POST.get('composition')
        traitement.mode_utilisation = request.POST.get('mode_utilisation')
        traitement.dosage = request.POST.get('dosage')
        traitement.quantite = request.POST.get('quantite')
        traitement.date_achat = request.POST.get('date_achat')
        traitement.cout = request.POST.get('cout')
        traitement.description = request.POST.get('description')
        traitement.geozone_id = request.POST.get('geozone')

        if 'image' in request.FILES:
            traitement.image = request.FILES['image']

        traitement.save()

        return JsonResponse({"success": "Engrais updated successfully"}, status=200)
    except Engrais_Tables.DoesNotExist:
        return JsonResponse({"error": "Engrais not found"}, status=404)
# Delete Traitement
def delete_traitement(request, traitement_id):
    try:
        traitement = Traitement_Tables.objects.get(id=traitement_id)
        traitement.delete()
        return JsonResponse({"success": "Traitements deleted successfully"}, status=200)
    except Traitement_Tables.DoesNotExist:
        return JsonResponse({"error": "Traitements not found"}, status=404)

""" Graines et Pousses """
# List Graines et Pousses
def graines_pousses (request):
    list = []
    graines = Graine_Tables.objects.filter(user=request.user)
    types_graines = TypeGrainesPousses.objects.all()
    categories_graines = CategorieGrainesPousses.objects.all()
    projects = MapForm.objects.all()
    list.append({"types": types_graines,"categories": categories_graines, "graines":graines, "projects": projects})
    return render(request, 'graines-pousses.html', {'data': list})
# List Tableau Graines et Pousses
def graines_pousses_list (request):
    list = []
    graines = Graine_Tables.objects.filter(user=request.user)
    types_graines = TypeGrainesPousses.objects.all()
    categories_graines = CategorieGrainesPousses.objects.all()
    projects = MapForm.objects.all()
    list.append({"types": types_graines,"categories": categories_graines, "graines":graines, "projects": projects})
    return render(request, 'graines-pousses-list.html', {'data': list})
# Save Graines et Pousses
@api_view(['POST'])
@authentication_classes([SessionAuthentication])  
@permission_classes([IsAuthenticated])
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
                "description": description,
                "user": request.user.id
            }
        
        graine_serializer = GraineSerializer(data=form)
                
        if graine_serializer.is_valid():
            print('yes')
            graine_serializer.save()
            return JsonResponse(graine_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('no')
            return JsonResponse({"Erreur": "Some error occured"}, status=status.HTTP_201_CREATED)
# Afficher Graines et Pousses       
def get_graine(request, graine_id):
    try:
        graine = Graine_Tables.objects.get(id=graine_id)
        project = MapForm.objects.filter(geozone=graine.geozone).first()
        data = {
            'id': graine.id,
            'nom': graine.nom,
            'type': graine.type,
            'categorie': graine.categorie,
            'origine': graine.origine,
            'quantite': graine.quantite,
            'cout': graine.cout,
            'geozone_name': project.project_name if project else 'No project found',  # Add project name
            'geozone_id': graine.geozone.id if graine.geozone else None,  # Add geozone ID
            'description': graine.description,
            'image': graine.image.url if graine.image else '',
        }
        return JsonResponse(data, status=200)
    except Graine_Tables.DoesNotExist:
        return JsonResponse({"error": "Graine not found"}, status=404)
# Details Graines et Pousses   
def get_graine_details(request, graine_id):
    try:
        graine = Graine_Tables.objects.get(id=graine_id)
        project = MapForm.objects.filter(geozone=graine.geozone).first()
        data = {
            'id': graine.id,
            'nom': graine.nom,
            'type': graine.type,
            'categorie': graine.categorie,
            'origine': graine.origine,
            'quantite': graine.quantite,
            'cout': graine.cout,
            'description': graine.description,
            'geozone': project.project_name if project else 'No project found',
            'image': graine.image.url if graine.image else '',
        }
        return JsonResponse(data, status=200)
    except Graine_Tables.DoesNotExist:
        return JsonResponse({"error": "Graine not found"}, status=404)
# Edit Graine details
def edit_graine(request, graine_id):
    try:
        graine = Graine_Tables.objects.get(id=graine_id)

        graine.nom = request.POST.get('nom')
        graine.type = request.POST.get('type_graines_pousses')
        graine.categorie = request.POST.get('categorie_graines_pousses')
        graine.origine = request.POST.get('origine')
        graine.quantite = request.POST.get('quantite')
        graine.cout = request.POST.get('cout')
        graine.description = request.POST.get('description')
        graine.geozone_id = request.POST.get('geozone')

        if 'image' in request.FILES:
            graine.image = request.FILES['image']

        graine.save()

        return JsonResponse({"success": "Graine updated successfully"}, status=200)
    except Graine_Tables.DoesNotExist:
        return JsonResponse({"error": "Graine not found"}, status=404)
# Delete Graine
def delete_graine(request, graine_id):
    try:
        graine = Graine_Tables.objects.get(id=graine_id)
        graine.delete()
        return JsonResponse({"success": "Graine deleted successfully"}, status=200)
    except Graine_Tables.DoesNotExist:
        return JsonResponse({"error": "Graine not found"}, status=404)

""" Ressources Humaines"""
def rh (request):
    list = []
    rhs = Rh_Tables.objects.filter(user=request.user)
    types_rhs = TypeRh.objects.all()
    projects = MapForm.objects.all()
    list.append({"types": types_rhs,"rhs": rhs, "projects": projects})
    return render(request, 'rh.html', {'data': list})

def rh_list (request):
    list = []
    rhs = Rh_Tables.objects.filter(user=request.user)
    types_rhs = TypeRh.objects.all()
    projects = MapForm.objects.all()
    list.append({"types": types_rhs,"rhs": rhs, "projects": projects})
    return render(request, 'rh-list.html', {'data': list})

@api_view(['POST'])
@authentication_classes([SessionAuthentication])  
@permission_classes([IsAuthenticated])
def save_rh(request):
    if request.method == "POST":
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        type = request.POST.get('type_rh')
        adresse = request.POST.get('adresse')
        num_tel = request.POST.get('telephone')
        email = request.POST.get('email')
        fonction = request.POST.get('fonction')
        salaire_heure = request.POST.get('salaire_heure')
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
                "geozone": geozone,
                "user": request.user.id
            }
        
        rh_serializer = RhSerializer(data=form)
                
        if rh_serializer.is_valid():
            print('yes')
            rh_serializer.save()
            return JsonResponse(rh_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('no')
            return JsonResponse({"Erreur": "Some error occured"}, status=status.HTTP_201_CREATED)

def get_rh(request, rh_id):
    try:
        rh = Rh_Tables.objects.get(id=rh_id)
        project = MapForm.objects.filter(geozone=rh.geozone).first()
        data = {
            'id': rh.id,
            'nom': rh.nom,
            'prenom': rh.prenom,
            'type': rh.type,
            'adresse': rh.adresse,
            'num_tel': rh.num_tel,
            'email': rh.email,
            'fonction': rh.fonction,
            'salaire_heure': rh.salaire_heure,
            'salaire_jour': rh.salaire_jour,
            'salaire_mois': rh.salaire_mois,
            'matricule_cnss': rh.matricule_cnss,
            'date_contrat': rh.date_contrat,
            'geozone_name': project.project_name if project else 'No project found',  # Add project name
            'geozone_id': rh.geozone.id if rh.geozone else None,  # Add geozone ID
            'image': rh.image.url if rh.image else '',
        }
        return JsonResponse(data, status=200)
    except Rh_Tables.DoesNotExist:
        return JsonResponse({"error": "Rh not found"}, status=404)  
# Edit Rh details
def edit_rh(request, rh_id):
    try:
        rh = Rh_Tables.objects.get(id=rh_id)

        rh.nom = request.POST.get('nom')
        rh.prenom = request.POST.get('prenom')
        rh.type = request.POST.get('type_rh')
        rh.adresse = request.POST.get('adresse')
        rh.num_tel = request.POST.get('num_tel')
        rh.email = request.POST.get('email')
        rh.fonction = request.POST.get('fonction')
        rh.salaire_heure = request.POST.get('salaire_heure')
        rh.salaire_jour = request.POST.get('salaire_jour')
        rh.salaire_mois = request.POST.get('salaire_mois')
        rh.matricule_cnss = request.POST.get('matricule_cnss')
        rh.date_contrat = request.POST.get('date_contrat')
        rh.geozone_id = request.POST.get('geozone')

        if 'image' in request.FILES:
            rh.image = request.FILES['image']

        rh.save()

        return JsonResponse({"success": "Rh updated successfully"}, status=200)
    except Rh_Tables.DoesNotExist:
        return JsonResponse({"error": "Rh not found"}, status=404)
# Afficher Rh details          
def get_rh_details(request, rh_id):
    try:
        rh = Rh_Tables.objects.get(id=rh_id)
        project = MapForm.objects.filter(geozone=rh.geozone).first()
        data = {
            'id': rh.id,
            'nom': rh.nom,
            'prenom': rh.prenom,
            'type': rh.type,
            'adresse': rh.adresse,
            'num_tel': rh.num_tel,
            'email': rh.email,
            'fonction': rh.fonction,
            'salaire_heure': rh.salaire_heure,
            'salaire_jour': rh.salaire_jour,
            'salaire_mois': rh.salaire_mois,
            'matricule_cnss': rh.matricule_cnss,
            'date_contrat': rh.date_contrat,
            'geozone': project.project_name if project else 'No project found',
            'image': rh.image.url if rh.image else '',
        }
        return JsonResponse(data, status=200)
    except Rh_Tables.DoesNotExist:
        return JsonResponse({"error": "Rh not found"}, status=404)
# Delete Rh
def delete_rh(request, rh_id):
    try:
        rh = Rh_Tables.objects.get(id=rh_id)
        rh.delete()
        return JsonResponse({"success": "Rh deleted successfully"}, status=200)
    except Rh_Tables.DoesNotExist:
        return JsonResponse({"error": "Rh not found"}, status=404)

""" pieces de rechange """
def pieces_rechange (request):
    list = []
    pieces = Pieces_Tables.objects.filter(user=request.user)
    types_pieces = TypePieces.objects.all()
    list.append({"types": types_pieces,"pieces": pieces})
    return render(request, 'pieces-rechange.html', {'data': list})

def pieces_rechange_list (request):
    list = []
    pieces = Pieces_Tables.objects.filter(user=request.user)
    types_pieces = TypePieces.objects.all()
    list.append({"types": types_pieces,"pieces": pieces})
    return render(request, 'pieces-rechange-list.html', {'data': list})

@api_view(['POST'])
@authentication_classes([SessionAuthentication])  
@permission_classes([IsAuthenticated])
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
                "image": image,
                "user": request.user.id
            }
        
        pieces_serializer = PiecesSerializer(data=form)
                
        if pieces_serializer.is_valid():
            print('yes')
            pieces_serializer.save()
            return JsonResponse(pieces_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('no')
            return JsonResponse({"Erreur": "Some error occured"}, status=status.HTTP_201_CREATED)
        
def get_piece(request, piece_id):
    try:
        piece = Pieces_Tables.objects.get(id=piece_id)
        data = {
            'id': piece.id,
            'nom': piece.nom,
            'type': piece.type,
            'cout': piece.cout,
            'date_achat': piece.date_achat,
            'image': piece.image.url if piece.image else None  
        }
        return JsonResponse(data)
    except Pieces_Tables.DoesNotExist:
        return JsonResponse({'error': 'Pièce non trouvée'}, status=404)

@require_http_methods(["POST", "PUT"])
def edit_piece(request, piece_id):
    try:
        piece = Pieces_Tables.objects.get(id=piece_id)

        if request.method == "POST":
            # Get data from form
            nom = request.POST.get('nom')
            type_piece = request.POST.get('type')  # Make sure 'type' is retrieved correctly
            cout = request.POST.get('cout')
            date_achat = request.POST.get('date_achat')

            # Ensure type is not null
            if not type_piece:
                return JsonResponse({"error": "Le type de pièce est obligatoire"}, status=400)

            # Update the piece fields
            piece.nom = nom
            piece.type = type_piece
            piece.cout = cout
            piece.date_achat = date_achat

            # Update image if provided
            if 'image' in request.FILES:
                piece.image = request.FILES['image']

            # Save the updated piece
            piece.save()

            return JsonResponse({"success": "Pièce modifiée avec succès"}, status=200)

    except Pieces_Tables.DoesNotExist:
        return JsonResponse({"error": "Pièce non trouvée"}, status=404)
        
# Delete Piece
def delete_piece(request, piece_id):
    try:
        piece = Pieces_Tables.objects.get(id=piece_id)
        piece.delete()
        return JsonResponse({"success": "piece deleted successfully"}, status=200)
    except Pieces_Tables.DoesNotExist:
        return JsonResponse({"error": "piece not found"}, status=404)
    
def get_piece_details(request, piece_id):
    try:
        piece = Pieces_Tables.objects.get(id=piece_id)
        data = {
            'nom': piece.nom,
            'type': piece.type,
            'cout': piece.cout,
            'date_achat': piece.date_achat,
            'image': piece.image.url if piece.image else '', 
        }
        return JsonResponse(data)
    except Pieces_Tables.DoesNotExist:
        return JsonResponse({'error': 'La pièce demandée n\'existe pas.'}, status=404)

""" carburant """
def carburant (request):
    list = []
    carburants = Carburants_Tables.objects.filter(user=request.user)
    #carburants = Carburants_Tables.objects.all()
    types_carburants = TypeCarburant.objects.all()
    list.append({"types": types_carburants,"carburants": carburants})
    return render(request, 'carburant.html', {'data': list})

def carburant_list (request):
    list = []
    carburants = Carburants_Tables.objects.filter(user=request.user)
    #carburants = Carburants_Tables.objects.all()
    types_carburants = TypeCarburant.objects.all()
    list.append({"types": types_carburants,"carburants": carburants})
    return render(request, 'carburant-list.html', {'data': list})

@require_http_methods(["DELETE"])
def delete_carburant(request, carburant_id):
    try:
        carburant = Carburants_Tables.objects.get(id=carburant_id)
        carburant.delete()
        return JsonResponse({"success": "Carburant supprimé avec succès"}, status=200)
    except Carburants_Tables.DoesNotExist:
        return JsonResponse({"error": "Carburant non trouvé"}, status=404)


@api_view(['POST'])
@authentication_classes([SessionAuthentication])  
@permission_classes([IsAuthenticated])
def save_carburant(request):
    if request.method == "POST":
        nom = request.POST.get('nom')
        type = request.POST.get('type_carburant')
        quantite = request.POST.get('quantite')
        cout = request.POST.get('cout')
        date_approvisionnement = request.POST.get('date_approvisionnement')

        # Check that the user is authenticated
        if request.user.is_authenticated:
            # Create a dictionary of the data including the user field (not user_id)
            form = {
                "nom": nom,
                "type": type,
                "quantite": quantite,
                "cout": cout,
                "date_approvisionnement": date_approvisionnement,
                "user": request.user.id  # Pass the user ID here correctly
            }

            # Use the serializer to validate and save
            carburant_serializer = CarburantsSerializer(data=form)
            
            if carburant_serializer.is_valid():
                carburant_serializer.save()  # This will save the instance to the DB
                return JsonResponse(carburant_serializer.data, status=status.HTTP_201_CREATED)
            else:
                # If data is not valid, return errors
                return JsonResponse({"Erreur": carburant_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Handle cases where the user is not authenticated
            return JsonResponse({"Erreur": "User not authenticated"}, status=status.HTTP_403_FORBIDDEN)

        
def get_carburant(request, carburant_id):
    try:
        carburant = Carburants_Tables.objects.get(id=carburant_id)
        data = {
            'id': carburant.id,
            'nom': carburant.nom,
            'type': carburant.type,
            'quantite': carburant.quantite,
            'cout': carburant.cout,
            'date_approvisionnement': carburant.date_approvisionnement,
        }
        return JsonResponse(data, status=200)
    except Carburants_Tables.DoesNotExist:
        return JsonResponse({"error": "Carburant non trouvé"}, status=404)
    
@require_http_methods(["PUT"])
def edit_carburant(request, carburant_id):
    try:
        carburant = Carburants_Tables.objects.get(id=carburant_id)
        
        data = json.loads(request.body)
        carburant.nom = data['nom']
        carburant.type = data['type']
        carburant.quantite = data['quantite']
        carburant.cout = data['cout']
        carburant.date_approvisionnement = data['date_approvisionnement']
        carburant.save()

        return JsonResponse({"success": "Carburant modifié avec succès"}, status=200)
    except Carburants_Tables.DoesNotExist:
        return JsonResponse({"error": "Carburant non trouvé"}, status=404)
    
def get_carburant_details(request, carburant_id):
    try:
        carburant = Carburants_Tables.objects.get(id=carburant_id)
        data = {
            'nom': carburant.nom,
            'type': carburant.type,
            'quantite': carburant.quantite,
            'cout': carburant.cout,
            'date_approvisionnement': carburant.date_approvisionnement
        }
        return JsonResponse(data, status=200)
    except Carburants_Tables.DoesNotExist:
        return JsonResponse({"error": "Carburant non trouvé"}, status=404)

""" Outils Agricoles"""
def outils_agricoles (request):
    list = []
    outils = Outils_Tables.objects.filter(user=request.user)
    types_outils = TypeOutilsAgricoles.objects.all()
    list.append({"types": types_outils,"outils": outils})
    return render(request, 'outils-agricoles.html', {'data': list})

def outils_agricoles_list (request):
    list = []
    outils = Outils_Tables.objects.filter(user=request.user)
    types_outils = TypeOutilsAgricoles.objects.all()
    list.append({"types": types_outils,"outils": outils})
    return render(request, 'outils-agricoles-list.html', {'data': list})

@api_view(['POST'])
@authentication_classes([SessionAuthentication])  
@permission_classes([IsAuthenticated])
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
                "allocation": allocation,
                "user": request.user.id
            }
        
        outils_serializer = OutilsSerializer(data=form)
                
        if outils_serializer.is_valid():
            print('yes')
            outils_serializer.save()
            return JsonResponse(outils_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('no')
            return JsonResponse({"Erreur": "Some error occured"}, status=status.HTTP_201_CREATED) 
        
def get_outil(request, outil_id):
    try:
        outil = Outils_Tables.objects.get(id=outil_id)
        data = {
            'id': outil.id,
            'type': outil.type,
            'numero_de_serie': outil.numero_de_serie,
            'marque': outil.marque,
            'allocation': outil.allocation,
            'prix_location_heure': outil.prix_location_heure,
            'prix_location_jour': outil.prix_location_jour,
            'prix_location_mois': outil.prix_location_mois,
            'date_location': outil.date_location,
            'prix_achat': outil.prix_achat,
            'date_achat': outil.date_achat,
            'image': outil.image.url if outil.image else None,  
            'description': outil.description,
        }
        return JsonResponse(data, status=200)
    except Outils_Tables.DoesNotExist:
        return JsonResponse({"error": "Outil non trouvé"}, status=404)
    
import logging
logger = logging.getLogger(__name__)

@require_http_methods(["POST"])
def edit_outil(request, outil_id):
    try:
        outil = Outils_Tables.objects.get(id=outil_id)
        
        # Retrieve form data and handle empty decimal fields
        outil.type = request.POST.get('type_outils_agricoles')
        outil.numero_de_serie = request.POST.get('numero_de_serie')
        outil.marque = request.POST.get('marque')
        outil.allocation = request.POST.get('allocation', 'non')

        # Handle empty values for decimal fields
        outil.prix_location_heure = request.POST.get('prix_location_heure') or None
        outil.prix_location_jour = request.POST.get('prix_location_jour') or None
        outil.prix_location_mois = request.POST.get('prix_location_mois') or None
        outil.date_location = request.POST.get('date_location')
        outil.prix_achat = request.POST.get('prix_achat') or None
        outil.date_achat = request.POST.get('date_achat')

        # Handle file upload
        if 'image' in request.FILES:
            outil.image = request.FILES['image']

        outil.description = request.POST.get('description')
        outil.save()

        return JsonResponse({"success": "Outil modifié avec succès"}, status=200)
    except Outils_Tables.DoesNotExist:
        return JsonResponse({"error": "Outil non trouvé"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@require_http_methods(["DELETE"])
def delete_outil(request, outil_id):
    try:
        outil = get_object_or_404(Outils_Tables, id=outil_id)
        outil.delete()
        return JsonResponse({"success": "Outil supprimé avec succès"}, status=200)
    except Outils_Tables.DoesNotExist:
        return JsonResponse({"error": "Outil non trouvé"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def get_outil_details(request, outil_id):
    try:
        outil = Outils_Tables.objects.get(id=outil_id)
        data = {
            'type': outil.type,
            'numero_de_serie': outil.numero_de_serie,
            'marque': outil.marque,
            'allocation': outil.allocation,
            'prix_location_heure': outil.prix_location_heure,
            'prix_location_jour': outil.prix_location_jour,
            'prix_location_mois': outil.prix_location_mois,
            'date_location': outil.date_location,
            'prix_achat': outil.prix_achat,
            'date_achat': outil.date_achat,
            'image': outil.image.url if outil.image else '',
            'description': outil.description,
        }
        return JsonResponse(data)
    except Outils_Tables.DoesNotExist:
        return JsonResponse({'error': 'Outil non trouvé'}, status=404)
        
""" Machines & Engins """
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

def machines_engins_new (request):
    return render(request, 'machines-engins-new.html')

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

def test (request): 
    return render(request, 'test.html')

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

def project_details(request, id):
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

    points_parcelles_map = []
    for zp in zones_parcelles:
        points_zp = serialize("json", PointParcelle.objects.all().filter(geozone_id=zp.pk))
        points_parcelles_map.append(points_zp)

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
    filters = serialize("json", Filtre.objects.all())
    colors = serialize("json", Color.objects.all())

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

    # Fetch filter options from the database
    filtre_humidite = FiltreHumidite.objects.all()
    filtre_irrigation = FiltreIrrigation.objects.all()
    filtre_fertilisation = FiltreFertilisation.objects.all()
    filtre_evolution = FiltreEvolution.objects.all()
    filtre_maladie = FiltreMaladie.objects.all()
    filtre_vegitation = FiltreVegitation.objects.all()

    filter_categories = {
        'végitation': filtre_vegitation,
        'humidité': filtre_humidite,
        'irrigation': filtre_irrigation,
        'fertilisation': filtre_fertilisation,
        'evolution': filtre_evolution,
        'maladie': filtre_maladie,
    }

    return render(request, 'project-details.html', {
        'data': dumped_data,
        'project': {'parcelles': parcelles},
        'filter_categories': filter_categories,
    })
    
def get_colors(request):
    filter_type = request.GET.get('filter')
    if filter_type == 'NDRE':
        colors = ColorReference.objects.all()
    elif filter_type == 'NDVI':
        colors = ColorReferenceNdvi.objects.all()
    elif filter_type == 'NDMI':
        colors = ColorReferenceNdmi.objects.all()
    elif filter_type == 'MSAVI':
        colors = ColorReferenceMsavi.objects.all()
    else:
        colors = []

    color_data = [{'value': color.value, 'color_css': color.color_css, 'description': color.description} for color in colors]
    return JsonResponse({'colors': color_data})

def get_points_for_parcelle(request, parcelle_id):
    points = PointParcelle.objects.filter(geozone_id=parcelle_id).values()
    return JsonResponse(list(points), safe=False)
       
""" def project_details (request, id):
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
    filterhs= serialize("json",FiltreHumidite.objects.all())
    print(filters)
    colors=  serialize("json",ColorReference.objects.all())
    print(colors)
    context = {
    'filters': filters,
    'filterhs': filterhs,
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
    return render(request, 'project-details.html', {'data': dumped_data,'project': {'parcelles': parcelles},}) """

def project_edit (request): 
    return render(request, 'project-edit.html')

@login_required
def project_new (request):
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
    except ObjectDoesNotExist:
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
    
@require_http_methods(["POST"])
def delete_project(request, project_id):
    try:
        project = MapForm.objects.get(id=project_id)
        project.delete()
        return JsonResponse({"message": "Projet supprimé avec succès"}, status=200)
    except MapForm.DoesNotExist:
        return JsonResponse({"error": "Projet introuvable"}, status=404)
    
def project_modifier(request, project_id):
    project = get_object_or_404(MapForm, id=project_id)

    if request.method == 'POST':
        # Récupérer les données soumises par le formulaire
        project.project_name = request.POST.get('project_name', project.project_name)
        project.project_date = request.POST.get('project_date', project.project_date)
        project.project_category = request.POST.get('project_category', project.project_category)
        project.department = request.POST.get('department', project.department)
        project.client = request.POST.get('client', project.client)

        # Sauvegarder les modifications dans la base de données
        project.save()

        # Rediriger vers la page des projets après la mise à jour
        return redirect('projects')  # Remplacez 'projects' par le nom de votre vue de liste des projets

    # Rendre la page de modification avec les données du projet
    return render(request, 'project-modifier.html', {'project': project})

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



def infrastructure (request):
    return render(request, 'infrastructure.html')
def fertilisants_traitements (request):
    return render(request, 'fertilisants-traitements.html')

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


def autres (request):
    return render(request, 'autres.html')

""" Operation Agricole """
def operations_utilisateur (request):
    operations = New_Oper_Tables.objects.all()
    cookie = request.COOKIES.get('jwtToken')
    if cookie:
        user_group = request.COOKIES.get('userGroup') or None
        context = {
            'jwtToken': cookie,
            'userGroup': user_group,
            'operations': operations,
        }
        print(context)
        return render(request, 'operations-utilisateur.html', context)
    else:
        return render(request, 'signin.html')

def get_points(request, geozone_id):
    points = Point.objects.filter(geozone_id=geozone_id)
    data = [{'latt': p.latt, 'long': p.long} for p in points]
    return JsonResponse(data, safe=False)

def ajouter_operation_agricole (request):
    list = []
    operations_agricoles = New_Oper_Tables.objects.all()
    type_rh = Rh_Tables.objects.all()
    projects = MapForm.objects.all()
    machines_tables = Machines_Tables.objects.all()
    type_carburant = TypeCarburant.objects.all()
    outil  =TypeOutilsAgricoles.objects.all()
    type_pieces  = TypePieces.objects.all()
    type_engrais  = TypeEngrais.objects.all() 
    type_graines_pousses  =TypeGrainesPousses.objects.all() 
    type_traitement = TypeTraitement.objects.all()
    list.append({"type_rh": type_rh,"machines_tables": machines_tables, "carburants": type_carburant, "outils": outil,"pieces": type_pieces,"graines" :type_graines_pousses,"engraiss" : type_engrais, "traitements" : type_traitement,   "operations": operations_agricoles, "projects": projects})
    return render(request, 'ajouter-operation-agricole.html', {'data': list})
   

def operation_view(request, id):
    operation = get_object_or_404(New_Oper_Tables, pk=id)
    main_doeuvres = operation.main_doeuvres.all()
    machine_carburants = operation.machine_carburants.all()
    outils = operation.outils.all()
    pieces = operation.pieces.all()
    # Retrieve markers associated with this operation
    markers = operation.markers.all()
    marker_data = [{'latitude': marker.latitude, 'longitude': marker.longitude} for marker in markers]

   # Retrieve points for the project zone
    project_points_data = []
    points = Point.objects.filter(geozone=operation.project.geozone)
    
    # Use the 'type' field from the 'Zone' model to determine shape
    shape_type = operation.project.geozone.type 

    if shape_type == 'circle':
        # Handle circle case
        center_point = points.first()  # Assuming a single point defines the circle center
        project_points_data.append({
            'type': 'circle',
            'center': {'latitude': center_point.latt, 'longitude': center_point.long},
            'radius': operation.project.geozone.circle_radius  # Use the radius from the zone
        })
    elif shape_type == 'polygon' or shape_type == 'rectangle':
        # Handle polygon or rectangle case
        project_points_data.append({
            'type': shape_type,
            'coordinates': [{'latitude': point.latt, 'longitude': point.long} for point in points]
        })
    else:
        # Handle individual points if no specific shape type is defined
        for point in points:
            project_points_data.append({
                'type': 'point',
                'latitude': point.latt,
                'longitude': point.long
            })

    context = {
        'operation': operation,
        'main_doeuvres': main_doeuvres,
        'machine_carburants': machine_carburants,
        'outils': outils,
        'pieces': pieces,
        'markers': marker_data,  
        'project_points': project_points_data,
    }
    return render(request, 'operation-view.html', context)
    
""" def operation_edit(request, id):
    operation = get_object_or_404(New_Oper_Tables, pk=id)
    if request.method == 'POST':
        # gérer la soumission du formulaire pour éditer l'opération
        pass
    return render(request, 'operation-edit.html', {'operation': operation}) """
    
def operation_edit(request, id):
    # Fetch the specific operation using the id
    operation = get_object_or_404(New_Oper_Tables, pk=id)
    main_doeuvres = operation.main_doeuvres.all()
    all_rh = Rh_Tables.objects.all()
    machine_carburants = operation.machine_carburants.all()
    machines_tables = Machines_Tables.objects.all()
    carburants = TypeCarburant.objects.all()
    outils = Tool.objects.all()
    selected_outils = operation.outils.all()
    type_engrais  = TypeEngrais.objects.all() 
    type_graines_pousses  =TypeGrainesPousses.objects.all() 
    type_traitement = TypeTraitement.objects.all()
    pieces = operation.pieces.all()  
    type_pieces = TypePieces.objects.all()
    
     # Retrieve markers associated with this operation
    markers = operation.markers.all()
    marker_data = [{'latitude': marker.latitude, 'longitude': marker.longitude} for marker in markers]

   # Retrieve points for the project zone
    project_points_data = []
    points = Point.objects.filter(geozone=operation.project.geozone)
    
    # Use the 'type' field from the 'Zone' model to determine shape
    shape_type = operation.project.geozone.type 

    if shape_type == 'circle':
        # Handle circle case
        center_point = points.first()  # Assuming a single point defines the circle center
        project_points_data.append({
            'type': 'circle',
            'center': {'latitude': center_point.latt, 'longitude': center_point.long},
            'radius': operation.project.geozone.circle_radius  # Use the radius from the zone
        })
    elif shape_type == 'polygon' or shape_type == 'rectangle':
        # Handle polygon or rectangle case
        project_points_data.append({
            'type': shape_type,
            'coordinates': [{'latitude': point.latt, 'longitude': point.long} for point in points]
        })
    else:
        # Handle individual points if no specific shape type is defined
        for point in points:
            project_points_data.append({
                'type': 'point',
                'latitude': point.latt,
                'longitude': point.long
            })

    if request.method == 'POST':
        # Updating Type d'opération
        operation.typeoperation = request.POST.get('typeoperation')
        operation.date_debut = request.POST.get('date_debut')
        operation.date_fin = request.POST.get('date_fin')
        
        # Mettre à jour les Graines, Fertilisants et Traitement
        operation.type_graines_pousses = request.POST.get('type_graines_pousses')
        operation.quantite_graine_utilisee = request.POST.get('quantite_graine_utilisee')
        
        operation.type_engrais = request.POST.get('type_engrais')
        operation.quantite_engrais_utilisee = request.POST.get('quantite_engrais_utilisee')
        
        operation.type_traitement = request.POST.get('type_traitement')
        operation.quantite_traitement_utilisee = request.POST.get('quantite_traitement_utilisee')
        
        # Mettre à jour la description
        operation.description = request.POST.get('description')
        
        operation.save()

        # Handling Main d'œuvre updates
        type_rh_list = request.POST.getlist('type_rh[]')
        time_list = request.POST.getlist('time[]')
        timefin_list = request.POST.getlist('timefin[]')

        # Clear old Main d'œuvre entries
        operation.main_doeuvres.clear()

        # Save updated Main d'œuvre entries
        for type_rh, time, timefin in zip(type_rh_list, time_list, timefin_list):
            if type_rh and time and timefin:
                try:
                    rh_instance = Rh_Tables.objects.get(pk=type_rh)
                    maindoeuvre_instance, _ = MainDoeuvre.objects.get_or_create(
                        type_rh=rh_instance, 
                        time=time, 
                        timefin=timefin
                    )
                    operation.main_doeuvres.add(maindoeuvre_instance)
                except Rh_Tables.DoesNotExist:
                    continue  # Handle the case where RH entry is not found
                
        # Machines et carburants handling
        type_machine_engins_list = request.POST.getlist('type_machine_engins[]')
        carburant_list = request.POST.getlist('carburant[]')
        quantite_carburant_list = request.POST.getlist('quantite_carburant[]')
        duree_utilisation_programme_list = request.POST.getlist('duree_utilisation_programme[]')
        heure_de_fin_list = request.POST.getlist('heure_de_fin[]')

        # Clear old machine_carburants
        operation.machine_carburants.clear()

        # Save new machine_carburants
        for type_machine_engins, carburant, quantite_carburant, duree_utilisation_programme, heure_de_fin in zip(
                type_machine_engins_list, carburant_list, quantite_carburant_list, duree_utilisation_programme_list, heure_de_fin_list):
            if type_machine_engins and carburant and quantite_carburant and duree_utilisation_programme and heure_de_fin:
                try:
                    machine_instance = Machines_Tables.objects.get(pk=type_machine_engins)
                    machine_carburant_instance, _ = MachineCarburant.objects.get_or_create(
                        type_machine_engins=machine_instance,
                        carburant=carburant,
                        duree_utilisation_programme=duree_utilisation_programme,
                        heure_de_fin=heure_de_fin,
                        quantite_carburant=quantite_carburant
                    )
                    operation.machine_carburants.add(machine_carburant_instance)
                except Machines_Tables.DoesNotExist:
                    continue
                
        # Handling Outil (Tools) updates
        outil_list = request.POST.getlist('outil[]')

        # Clear old outils entries for this operation
        operation.outils.clear()

        # Save updated outils entries
        for outil_id in outil_list:
            try:
                outil_instance = Tool.objects.get(pk=outil_id)
                operation.outils.add(outil_instance)
            except Tool.DoesNotExist:
                continue
            
        # Handle Pieces de Rechange updates
        type_pieces_list = request.POST.getlist('type_pieces[]')
        nombre_de_pieces_list = request.POST.getlist('nombre_de_pieces[]')

        # Clear old pieces entries
        operation.pieces.clear()

        # Enregistrer les nouvelles pièces
        for type_piece_id, nombre_de_pieces in zip(type_pieces_list, nombre_de_pieces_list):
            if type_piece_id and nombre_de_pieces:
                try:
                    # Récupérer la pièce par son identifiant
                    piece_instance = PieceDeRechange.objects.get(pk=type_piece_id)
                    # Mettre à jour le nombre de pièces
                    piece_instance.nombre_de_pieces = nombre_de_pieces
                    piece_instance.save()
                    # Ajouter la pièce à l'opération
                    operation.pieces.add(piece_instance)
                except PieceDeRechange.DoesNotExist:
                    continue
                
        # Traitement du marker
        marker_lat = request.POST.get('marker_lat')
        marker_lng = request.POST.get('marker_lng')
        
        # Mettre à jour les coordonnées du marker
        for marker in markers:
            marker.latitude = marker_lat
            marker.longitude = marker_lng
            marker.save()
        
        
        return redirect('operation-view', id=operation.id)

    context = {
        'operation': operation,
        'main_doeuvres': main_doeuvres,
        'all_rh': all_rh,
        'machines_tables': machines_tables,
        'machine_carburants': machine_carburants,
        'carburants': carburants,
        'outils': outils,
        'selected_outils_ids': [outil.id for outil in selected_outils],
        'type_engrais': type_engrais,
        'type_graines_pousses': type_graines_pousses,
        'type_traitement': type_traitement,
        'pieces': pieces,
        'type_pieces': type_pieces,
        'markers': markers,
        'markers': marker_data,  
        'project_points': project_points_data,
    }
    return render(request, 'operation-edit.html', context)


def operation_delete(request, id):
    operation = get_object_or_404(New_Oper_Tables, id=id)
    operation.delete()
    return redirect(reverse('operations-utilisateur'))

@api_view(['POST'])
def save_operation(request):
    if request.method == "POST":
        project_id = request.POST.get('project_id')
        typeoperation = request.POST.get('typeoperation')
        date_debut = request.POST.get('date_debut')
        date_fin = request.POST.get('date_fin')
        
        type_rh_list = request.POST.getlist('type_rh[]')
        time_list = request.POST.getlist('time[]')
        timefin_list = request.POST.getlist('timefin[]')

        type_machine_engins_list = request.POST.getlist('type_machine_engins[]')
        carburant_list = request.POST.getlist('carburant[]')
        duree_utilisation_programme_list = request.POST.getlist('duree_utilisation_programme[]')
        heure_de_fin_list = request.POST.getlist('heure_de_fin[]')
        quantite_carburant_list = request.POST.getlist('quantite_carburant[]')

        outils = request.POST.getlist('outil[]')
        pieces = request.POST.getlist('type_pieces[]')
        quantities = request.POST.getlist('nombre_de_pieces[]')

        type_graines_pousses = request.POST.get('type_graines_pousses')
        quantite_graine_utilisee = request.POST.get('quantite_graine_utilisee')
        type_engrais = request.POST.get('type_engrais')
        quantite_engrais_utilisee = request.POST.get('quantite_engrais_utilisee')
        type_traitement = request.POST.get('type_traitement')
        quantite_traitement_utilisee = request.POST.get('quantite_traitement_utilisee')
        description = request.POST.get('description')
        
        # Retrieve marker data
        marker_latitudes = request.POST.getlist('marker_latitude[]')
        marker_longitudes = request.POST.getlist('marker_longitude[]')

        # Validate required fields
        if not project_id or not typeoperation:
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        try:
            # Retrieve the project object
            project = MapForm.objects.get(geozone_id=project_id)
        except MapForm.DoesNotExist:
            return JsonResponse({'error': 'Project not found'}, status=400)

        # Create the agricultural operation
        operation = New_Oper_Tables.objects.create(
            project=project,
            typeoperation=typeoperation,
            date_debut=date_debut,
            date_fin=date_fin,
            type_graines_pousses=type_graines_pousses,
            quantite_graine_utilisee=quantite_graine_utilisee,
            type_engrais=type_engrais,
            quantite_engrais_utilisee=quantite_engrais_utilisee,
            type_traitement=type_traitement,
            quantite_traitement_utilisee=quantite_traitement_utilisee,
            description=description
        )

        # Add tools (outils) to the operation
        for outil in outils:
            tool_instance, _ = Tool.objects.get_or_create(name=outil)
            operation.outils.add(tool_instance)

        # Add spare parts (pieces) to the operation
        for piece, quantity in zip(pieces, quantities):
            piece_instance, _ = PieceDeRechange.objects.get_or_create(type_pieces=piece, nombre_de_pieces=quantity)
            operation.pieces.add(piece_instance)

        # Add labor (main d'oeuvre) to the operation
        for type_rh, time, timefin in zip(type_rh_list, time_list, timefin_list):
            try:
                rh_instance = Rh_Tables.objects.get(pk=type_rh)
                maindoeuvre_instance, _ = MainDoeuvre.objects.get_or_create(type_rh=rh_instance, time=time, timefin=timefin)
                operation.main_doeuvres.add(maindoeuvre_instance)
            except Rh_Tables.DoesNotExist:
                return JsonResponse({"error": f"RH with id {type_rh} not found"}, status=400)

        # Add machines and fuel (machine_carburants) to the operation
        for type_machine_engins, carburant, duree_utilisation_programme, heure_de_fin, quantite_carburant in zip(
                type_machine_engins_list, carburant_list, duree_utilisation_programme_list, heure_de_fin_list, quantite_carburant_list):
            try:
                machine_instance = Machines_Tables.objects.get(pk=type_machine_engins)
                machine_carburant_instance, _ = MachineCarburant.objects.get_or_create(
                    type_machine_engins=machine_instance,
                    carburant=carburant,
                    duree_utilisation_programme=duree_utilisation_programme,
                    heure_de_fin=heure_de_fin,
                    quantite_carburant=quantite_carburant
                )
                operation.machine_carburants.add(machine_carburant_instance)
            except Machines_Tables.DoesNotExist:
                return JsonResponse({"error": f"Machine with id {type_machine_engins} not found"}, status=400)
            
        # Save markers
        for lat, lng in zip(marker_latitudes, marker_longitudes):
            marker = Marker.objects.create(
                project=project,
                latitude=lat,
                longitude=lng
            )
            operation.markers.add(marker)

        # Check if the operation was created successfully
        if operation and operation.pk:
            return JsonResponse({'message': 'Operation saved successfully!'}, status=201)
        else:
            return JsonResponse({"error": "Failed to save the operation"}, status=400)

@csrf_exempt
@api_view(['POST'])
def save_marker(request):
    if request.method == 'POST':
        data = request.data
        project_id = data.get('project_id')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        try:
            project = MapForm.objects.get(geozone_id=project_id)
            print(project)
            marker = Marker.objects.create(
                project=project,
                latitude=latitude,
                longitude=longitude
            )
            return JsonResponse({'id': marker.id, 'message': 'Marker saved successfully!'}, status=201)
        except MapForm.DoesNotExist:
            return JsonResponse({'error': 'Project not found'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

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

import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['image']
     
def preprocess_image_for_red_text(image_path):
    image = Image.open(image_path).convert("RGB")
    np_image = np.array(image)

    # Extract red channel
    red_channel = np_image[:, :, 0]
    green_channel = np_image[:, :, 1]
    blue_channel = np_image[:, :, 2]

    # Create a mask for red areas
    red_mask = (red_channel > 150) & (green_channel < 100) & (blue_channel < 100)
    
    # Apply mask to get image with only red text
    red_text_image = np.zeros_like(np_image)
    red_text_image[red_mask] = [255, 255, 255]  # Set red text to white
    red_text_image[~red_mask] = [0, 0, 0]      # Set other areas to black
    
    # Convert back to PIL Image
    processed_image = Image.fromarray(red_text_image)
    return processed_image 

from django.db.models import Q

def analyse(request):
    query = request.GET.get('q')
    sort_by = request.GET.get('sort_by')
    images = UploadedImage.objects.all().order_by('-id')

    if query:
        # Filtrer les images en fonction du nom de la maladie
        images = images.filter(disease_name__icontains=query)
        
    if sort_by:
        if sort_by == 'date_desc':
            images = images.order_by('-id')
        elif sort_by == 'date_asc':
            images = images.order_by('id')
        elif sort_by == 'disease_name_asc':
            images = images.order_by('disease_name')
        elif sort_by == 'disease_name_desc':
            images = images.order_by('-disease_name')

    paginator = Paginator(images, 12)

    # Retrieve all plant names to populate the dropdown
    plants = CategoriesPlantes.objects.all()

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save()
            image_path = uploaded_image.image.path
            with open(image_path, 'rb') as image_file:
                files = {'file': image_file}
                ngrok_url = 'https://bcd4-34-147-114-245.ngrok-free.app/predict'
                response = requests.post(ngrok_url, files=files)
                if response.status_code == 200:
                    result_image_dir = 'D:/MAGON_3SSS/MAGON_3SSS/MAGON_3SSS-main/MAGON_3S/static/assets/results/'
                    result_image_name = f'result_{uploaded_image.id}.png'
                    result_image_path = os.path.join(result_image_dir, result_image_name)
                    with open(result_image_path, 'wb') as f:
                        f.write(response.content)
                    uploaded_image.result_image.name = os.path.join('/results', result_image_name)

                    # Prétraitement et OCR pour extraire le nom de la maladie
                    processed_image = preprocess_image_for_red_text(result_image_path)
                    ocr_result = pytesseract.image_to_string(processed_image, config='--psm 6')
                    disease_name = ocr_result.strip()

                    uploaded_image.disease_name = disease_name
                    uploaded_image.save()

                    return JsonResponse({'success': True, 'image_url': uploaded_image.result_image.url, 'disease_name': disease_name})
                else:
                    return JsonResponse({'success': False, 'error_message': 'Erreur lors du traitement de l\'image'})
        else:
            return JsonResponse({'success': False, 'error_message': 'Formulaire invalide'})
    else:
        form = ImageUploadForm()

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'analyse.html', {'form': form, 'images': images, 'page_obj': page_obj, 'plants': plants})

""" def analyse(request):
    images = UploadedImage.objects.all().order_by('-id')
    paginator = Paginator(images, 12)
    
    # Retrieve all plant names to populate the dropdown
    plants = CategoriesPlantes.objects.all()
    
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save()
            image_path = uploaded_image.image.path
            with open(image_path, 'rb') as image_file:
                files = {'file': image_file}
                ngrok_url = 'https://8815-34-132-1-102.ngrok-free.app/predict'
                response = requests.post(ngrok_url, files=files)
                if response.status_code == 200:
                    result_image_dir = 'D:/MAGON_3SSS/MAGON_3SSS/MAGON_3SSS-main/MAGON_3S/static/assets/results/'
                    result_image_name = f'result_{uploaded_image.id}.png'
                    result_image_path = os.path.join(result_image_dir, result_image_name)
                    with open(result_image_path, 'wb') as f:
                        f.write(response.content)
                    uploaded_image.result_image.name = os.path.join('/results', result_image_name)
                    
                    # Preprocess and perform OCR on the result image to extract the disease name
                    processed_image = preprocess_image_for_red_text(result_image_path)
                    ocr_result = pytesseract.image_to_string(processed_image, config='--psm 6')
                    disease_name = ocr_result.strip()
                    
                    uploaded_image.disease_name = disease_name
                    uploaded_image.save()
                    
                    return JsonResponse({'success': True, 'image_url': uploaded_image.result_image.url, 'disease_name': disease_name})
                else:
                    return JsonResponse({'success': False, 'error_message': 'Erreur lors du traitement de l\'image'})
        else:
            return JsonResponse({'success': False, 'error_message': 'Formulaire invalide'})
    else:
        form = ImageUploadForm()
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    
    return render(request, 'analyse.html', {'form': form, 'images': images, 'page_obj': page_obj, 'plants': plants}) """

def get_subcategories(request):
    category_id = request.GET.get('category_id')

    if category_id == '1':  # Assuming Olive has id 1
        subcategories = SousCategoriesOlives.objects.all()
    elif category_id == '2':  # Assuming Palmier has id 2
        subcategories = SousCategoriesPalmier.objects.all()
    elif category_id == '3':  # Assuming Pomme de Terre has id 3
        subcategories = SousCategoriesPommeDeTerre.objects.all()
    else:
        subcategories = []

    subcategories_data = [{'id': sub.id, 'name': sub.nom_souscategorie_olive if category_id == '1' else sub.nom_souscategorie_palmier if category_id == '2' else sub.nom_souscategorie_pomme_terre} for sub in subcategories]

    return JsonResponse({'subcategories': subcategories_data})

def get_anomalies(request):
    category_id = request.GET.get('category_id')

    if category_id == '1':  # Assuming Olive has id 1
        anomalies = Anomaly.objects.all()
    elif category_id == '2':  # Assuming Palmier has id 2
        anomalies = AnomalyPalmier.objects.all()
    elif category_id == '3':  # Assuming Pomme de Terre has id 3
        anomalies = AnomalyPommeDeTerre.objects.all()
    else:
        anomalies = []

    anomalies_data = [{'id': anomaly.id, 'name': anomaly.nom} for anomaly in anomalies]

    return JsonResponse({'anomalies': anomalies_data})

""" class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['image']
        
def analyse(request):
    images = UploadedImage.objects.all()
    paginator = Paginator(images, 12)
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save()
            image_path = uploaded_image.image.path
            with open(image_path, 'rb') as image_file:
                files = {'file': image_file}
                ngrok_url = 'https://b635-34-106-208-190.ngrok-free.app/predict'
                response = requests.post(ngrok_url, files=files)
                if response.status_code == 200:
                    result_image_dir = 'D:/MAGON_3SSS/MAGON_3SSS/MAGON_3SSS-main/MAGON_3S/static/assets/results/'
                    result_image_name = f'result_{uploaded_image.id}.png'
                    result_image_path = os.path.join(result_image_dir, result_image_name)
                    with open(result_image_path, 'wb') as f:
                        f.write(response.content)
                    uploaded_image.result_image.name = os.path.join('/results', result_image_name)
                    uploaded_image.save()
                    return JsonResponse({'success': True, 'image_url': uploaded_image.result_image.url})
                else:
                    return JsonResponse({'success': False, 'error_message': 'Erreur lors du traitement de l\'image'})
        else:
            return JsonResponse({'success': False, 'error_message': 'Formulaire invalide'})
    else:
        form = ImageUploadForm()
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)   
    return render(request, 'analyse.html', {'form': form, 'images': images, 'page_obj': page_obj}) """ 

def analyse_details(request, image_id):
    cookie = request.COOKIES.get('jwtToken')
    if cookie:
        user_group = request.COOKIES.get('userGroup') or None
        # Récupérer les quatre premières images avec un résultat
        images = UploadedImage.objects.exclude(result_image__isnull=True).exclude(result_image__exact='').order_by('-id')[:4]
        result_image = get_object_or_404(UploadedImage, id=image_id)
        # Fetch the Anomaly object based on the disease_name in UploadedImage
        anomaly = None
        if result_image.disease_name:
            anomaly = Anomaly.objects.filter(nom=result_image.disease_name).first()
        context = {
            'jwtToken': cookie,
            'userGroup': user_group,
            'images': images,
            'result_image': result_image,
            'anomaly': anomaly,
        }
        print(context)
        return render(request, 'analyse-details.html', context)
    else: 
        return render(request, 'signin.html')
    
""" def analyse_details (request):
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
        return render(request, 'signin.html') """
    
@require_http_methods(["DELETE"])
def delete_item(request, item_id):
    try:
        item = UploadedImage.objects.get(id=item_id)
        item.delete()
        return JsonResponse({'success': True})
    except UploadedImage.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Item does not exist'}, status=404)
        
""" def analyse (request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save()
            image_path = uploaded_image.image.path

            with open(image_path, 'rb') as image_file:
                files = {'file': image_file}

                # Remplacez 'NGROK_PUBLIC_URL' par l'URL réelle de votre service Ngrok
                ngrok_url = 'https://6cdc-104-155-157-48.ngrok-free.app/predict'
                response = requests.post(ngrok_url, files=files)

                if response.status_code == 200:
                    # Chemin complet pour sauvegarder l'image traitée
                    result_image_dir = 'D:/MAGON_3SSS/MAGON_3SSS/MAGON_3SSS-main/MAGON_3S/static/assets/results/'
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
    return render(request, 'analyse.html', {'form': form}) """
