import datetime
import os
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Permission, Group
from django.apps import AppConfig
from django.contrib.contenttypes.models import ContentType
from django import forms
#from app.models import MyModel

# Create your models here.

#####################


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/')
    designation = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    website = models.URLField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(max_length=150, blank=True, null=True)
    
class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image']
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image', 'designation', 'website', 'phone', 'address']
        
    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save(update_fields=self.changed_data)
        return profile
        
class ProfileCompany(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    companyname = models.CharField(max_length=255, blank=True)
    activity = models.CharField(max_length=255, blank=True)
    matricule = models.CharField(max_length=20, blank=True)
    address_company = models.TextField(max_length=255, blank=True)
    country = models.CharField(max_length=50, blank=True)
    website_company = models.URLField(max_length=200, blank=True)
    phoneNumber = models.CharField(max_length=15, blank=True, null=True)
    area = models.CharField(max_length=100, blank=True)
    type_of_agriculture = models.CharField(max_length=100, blank=True)
    logo = models.ImageField(upload_to='company_logos/')
    
class ProfileCompanyForm(forms.ModelForm):
    class Meta:
        model = ProfileCompany
        fields = [ 'companyname', 'activity', 'matricule', 'address_company', 'country', 'website_company', 'phoneNumber', 'area', 'type_of_agriculture', 'logo']

####################
        
""" class TypeOperationAgricole(models.Model):
    type_operation_agricole=models.CharField(max_length=50) """
    
class LogistiquesPermission(models.Model):
    class Meta:
        permissions = [
            ("view_logistiques", "Can view logistiques"),
        ]
        
class ProjectsPermission(models.Model):
    class Meta:
        permissions = [
            ("view_projects", "Can view projects"),
        ]
    
class Zone(models.Model):
    type=models.CharField(max_length=50)
    area=models.CharField(max_length=100)
    circle_radius=models.CharField(max_length=100)
 
class Point(models.Model):
    latt=models.CharField(max_length=50)
    long=models.CharField(max_length=50)
    geozone = models.ForeignKey(Zone,on_delete=models.CASCADE)
    
class MapForm(models.Model):
    project_name=models.CharField(max_length=100)
    project_date=models.CharField(max_length=100)
    project_category=models.CharField(max_length=20)
    department=models.CharField(max_length=50)
    client=models.CharField(max_length=50)
    geozone= models.ForeignKey(Zone,on_delete=models.CASCADE)
        
class ZoneParcelle(models.Model):
    type=models.CharField(max_length=50)
    area=models.CharField(max_length=100)
    circle_radius=models.CharField(max_length=100)
    id_projet=models.TextField()
    
 
class PointParcelle(models.Model):
    latt=models.CharField(max_length=50)
    long=models.CharField(max_length=50)
    geozone = models.ForeignKey(ZoneParcelle,on_delete=models.CASCADE)
    
    
class MapFormParcelle(models.Model):
    parcelle_name=models.CharField(max_length=100)
    parcelle_date=models.CharField(max_length=100)
    parcelle_category=models.CharField(max_length=20)
    department=models.CharField(max_length=50)
    client=models.CharField(max_length=50,)
    geozone = models.ForeignKey(ZoneParcelle,on_delete=models.CASCADE)
    id_projet=models.TextField()
    
class Filtre(models.Model):
    abreviation=models.CharField(max_length=50)
    descriptionFr=models.TextField()
    descriptionAr=models.TextField()
       
class ColorReference(models.Model):
    value=models.CharField(max_length=50)
    color_css=models.CharField(max_length=50)
    description=models.TextField(null=True)
    
def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now()
    filename="%s %s" % (timeNow, old_filename)
    return os.path.join('uploads/', filename)

    
class Machines_Tables(models.Model):
    type = models.CharField(max_length=50)
    matricule = models.CharField(max_length=255)
    marque = models.CharField(max_length=255)
    carte_grise = models.CharField(max_length=255)
    date_assurance = models.CharField(max_length=100)
    date_visite = models.CharField(max_length=100)
    date_vignette = models.CharField(max_length=100)
    allocation = models.CharField(max_length=3)
    prix_heure = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    prix_jour = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    prix_mois = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date_location = models.CharField(max_length=100, null=True, blank=True)
    prix_achat = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date_achat = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to=filepath , null=True, blank=True)
    description = models.TextField(null=True)
    
class Outils_Tables(models.Model):
    type = models.CharField(max_length=50)
    numero_de_serie = models.CharField(max_length=255)
    marque = models.CharField(max_length=255)
    allocation = models.CharField(max_length=3)
    prix_location_heure = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    prix_location_jour = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    prix_location_mois = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date_location = models.CharField(max_length=100, null=True, blank=True)
    prix_achat = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date_achat = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to=filepath , null=True, blank=True)
    description = models.TextField(null=True)
    
class Carburants_Tables(models.Model):
    nom = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    quantite = models.CharField(max_length=255)
    cout = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date_approvisionnement = models.CharField(max_length=100, null=True, blank=True)
       
class Pieces_Tables(models.Model):
    nom = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    cout = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date_achat = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to=filepath , null=True, blank=True)
    
class Rh_Tables(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    adresse = models.CharField(max_length=255)
    num_tel = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    fonction = models.CharField(max_length=100)
    salaire_heure = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salaire_jour = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salaire_mois = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    matricule_cnss = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to=filepath , null=True, blank=True)
    date_contrat = models.CharField(max_length=100, null=True, blank=True)
    geozone = models.ForeignKey(Zone,on_delete=models.CASCADE)

class Graine_Tables(models.Model):
    nom = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    categorie = models.CharField(max_length=255)
    origine = models.CharField(max_length=50)
    quantite = models.CharField(max_length=100)
    cout = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to=filepath , null=True, blank=True)
    geozone = models.ForeignKey(Zone,on_delete=models.CASCADE)
    description = models.TextField(null=True)

class Traitement_Tables(models.Model):
    nom = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    categorie = models.CharField(max_length=255)
    composition = models.CharField(max_length=50)
    mode_utilisation = models.CharField(max_length=100)
    dosage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantite = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date_achat = models.CharField(max_length=100, null=True, blank=True)
    cout = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to=filepath , null=True, blank=True)
    geozone = models.ForeignKey(Zone,on_delete=models.CASCADE)
    description = models.TextField(null=True)
    
class Engrais_Tables(models.Model):
    nom = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    categorie = models.CharField(max_length=255)
    composition = models.CharField(max_length=50)
    mode_utilisation = models.CharField(max_length=100)
    dosage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantite = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date_achat = models.CharField(max_length=100, null=True, blank=True)
    cout = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to=filepath , null=True, blank=True)
    geozone = models.ForeignKey(Zone,on_delete=models.CASCADE)
    description = models.TextField(null=True)
    
""" class Moteur_Tables(models.Model):
    nom=models.CharField(max_length=30)
    marque=models.CharField(max_length=30)
    type_moteur=models.CharField(max_length=50)
    puissance=models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    type_tension=models.CharField(max_length=50)
    tension=models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    type_couplage=models.CharField(max_length=50)
    courant=models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    geozone = models.ForeignKey(Zone,on_delete=models.CASCADE) """
    
class Maison_Tables(models.Model):
    nom = models.CharField(max_length=100)
    
class Frigo_Tables(models.Model):
    nom = models.CharField(max_length=100)
    
class Hangar_Tables(models.Model):
    nom = models.CharField(max_length=100)       
  
class TypeMachineEngins(models.Model):
    type_machine_engins=models.CharField(max_length=50)
    
class TypeOutilsAgricoles(models.Model):
    type_outils_agricoles=models.CharField(max_length=50)
    
class TypePuit(models.Model):
    type_puit=models.CharField(max_length=50)
 
class TypeReservoir(models.Model):
    type_reservoir=models.CharField(max_length=50)
    
class TypeVanne(models.Model):
    type_vanne=models.CharField(max_length=50)
    
class SectionVanne(models.Model):
    section_vanne=models.CharField(max_length=50)
    
class TypePivot(models.Model):
    type_pivot=models.CharField(max_length=50)
    
class TypePulverisateuraxiale(models.Model):
    type_pulverisateur_axiale=models.CharField(max_length=50)
    
class TypeCompteurPoste(models.Model):
    type_compteur_poste=models.CharField(max_length=50)
    
class TypeTensionGenerateur(models.Model):
    type_tension_generateur=models.CharField(max_length=50)
    
class TypeCarburantGenerateur(models.Model):
    type_carburant_generateur=models.CharField(max_length=50)
    
class TypeMoteur(models.Model):
    type_moteur=models.CharField(max_length=50)
    
class TypeTensionMoteur(models.Model):
    type_tension_moteur=models.CharField(max_length=50)
    
class TypeCouplageMoteur(models.Model):
    type_couplage_moteur=models.CharField(max_length=50)
    
class TypeSvsCamera(models.Model):
    type_svs_camera=models.CharField(max_length=50)
    
class MarqueDvrNvr(models.Model):
    marque_dvr_nvr=models.CharField(max_length=50)
    
class NbrChaineDvrNvr(models.Model):
    nbr_chaine_dvr_nvr=models.CharField(max_length=50)
    
class AlimentationCamera(models.Model):
    alimentation_camera=models.CharField(max_length=50)
    
class TypeAntiIncendie(models.Model):
    type_anti_incendie=models.CharField(max_length=50)
    
class TypeDetectionIntrusion(models.Model):
    type_detection_intrusion=models.CharField(max_length=50)
    
class TypeControleAcces(models.Model):
    type_controle_acces=models.CharField(max_length=50)
    
class MarqueControleAcces(models.Model):
    marque_controle_acces=models.CharField(max_length=50)
    
class TypeMaisonVilla(models.Model):
    type_Maison_Villa=models.CharField(max_length=50)
    
class TypeHangerDepot(models.Model):
    type_hanger_depot=models.CharField(max_length=50)
          
class TypeFrigo(models.Model):
    type_frigo=models.CharField(max_length=50)
    
class TypeEngrais(models.Model):
    type_engrais=models.CharField(max_length=50)
    
class CategorieEngrais(models.Model):
    categorie_engrais=models.CharField(max_length=50)
    
class TypeTraitement(models.Model):
    type_traitement=models.CharField(max_length=50)
    
class CategorieTraitement(models.Model):
    categorie_traitement=models.CharField(max_length=50)
 
class TypeGrainesPousses(models.Model):
    type_graines_pousses=models.CharField(max_length=50)
    
class CategorieGrainesPousses(models.Model):
    categorie_graines_pousses=models.CharField(max_length=50)
    
class TypeCarburant(models.Model):
    type_carburant=models.CharField(max_length=50)
    
class TypePieces(models.Model):
    type_pieces=models.CharField(max_length=50)
    
class TypeRh(models.Model):
    type_rh=models.CharField(max_length=50)
    
class Test(models.Model):
    type=models.CharField(max_length=50)
    nom=models.CharField(max_length=50)   
    