from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from app.views import CustomTokenObtainPairView, savezone
from app.views import save_form
from app.views import savezoneparcelle
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from app.views import UserAPIView
from app.views import SidebarView
from app.views import logistiques, check_logistiques_access
from django.contrib.auth import views as auth_views
from .views import popup_view
#from app.views import MyTokenObtainPairView
#from .views import sentinelhub_api_example

#app_name = 'app'

urlpatterns = [
    path('', views.landing_page, name='landing-page'),   
    path('sidebar/', SidebarView.as_view(), name='app-sidebar'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('api/test/refresh/',TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user/', UserAPIView.as_view(), name='user'),
    path('signin', views.signin, name='signin'),
    path('save/',savezone),
    path('save2/',save_form),
    path('get/zone/<int:pk>/',views.get_zone),
    path('get/points/<int:pk>/',views.get_point),
    #path('sentinelhub-api-example/', views.sentinel_hub_view, name='sentinel_hub_view'),
    #path('sentinelhub-api-example/', views.sentinelhub_api_example(time_interval=('2023-01-01', '2023-01-02')), name='sentinelhub_api_example'),
    path('saveparcelle/',savezoneparcelle),
    path('saveFormParcelle/',views.save_form_parcelle),
    
    path('api/save_operation/', views.save_operation, name='save_operation'),
    path('api/get-points/<int:geozone_id>/', views.get_points, name='get_points'),
    
    path('sentinelhub-raster-image/', views.generate_raster_image, name='sentinelhub-raster-image'),
    path('saveMachine/',views.save_machine, name='save_machine'),
    path('saveOutil/',views.save_outil),
    path('saveCarburant/',views.save_carburant),
    path('savepieces/',views.save_pieces),
    path('saveRh/',views.save_rh),
    path('saveGraine/',views.save_graine),
    path('saveTraitement/',views.save_traitement),
    path('saveEngrais/',views.save_engrai),
    path('saveMoteur/',views.save_moteur),
     
    path('register1',views.register1, name='register1'), 
    path('register',views.register, name='register'), 
    #path('signin', views.signin, name='signin'),    
    path('signout', views.signout, name='signout'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
              
    path('abouthome', views.abouthome, name='abouthome'),
    path('home', views.home, name='home'),
    path('profile-user', views.profile_user, name='profile-user'),
    path('edit-profile', views.edit_profile, name='edit-profile'),
    path('profile-update/', views.profile_update, name='profile-update'),
    path('update-profile-image/', views.update_profile_image, name='update-profile-image'),
    path('update-company-info/', views.update_company_info, name='update-company-info'),
    
    path('test', views.test, name='test'),
    path('about', views.about, name='about'),
    path('accordion', views.accordion, name='accordion'),
    path('alerts', views.alerts, name='alerts'),
    path('avatar', views.avatar, name='avatar'),
    path('background', views.background, name='background'),
    path('badge', views.badge, name='badge'),
    path('blog-details', views.blog_details, name='blog-details'),
    path('blog-edit', views.blog_edit, name='blog-edit'),
    path('blog', views.blog, name='blog'),
    path('border', views.border, name='border'),
    path('breadcrumbs', views.breadcrumbs, name='breadcrumbs'),
    path('buttons', views.buttons, name='buttons'),
    path('calendar2', views.calendar2, name='calendar2'),
    path('cards', views.cards, name='cards'),
    path('carousel', views.carousel, name='carousel'),
    path('cart', views.cart, name='cart'),
    path('chart-chartjs', views.chart_chartjs, name='chart-chartjs'),
    path('chart-echart', views.chart_echart, name='chart-echart'),
    path('chart-flot', views.chart_flot, name='chart-flot'),
    path('chart-morris', views.chart_morris, name='chart-morris'),
    path('chart-nvd3', views.chart_nvd3, name='chart-nvd3'),
    path('chat', views.chat, name='chat'),
    path('checkout', views.checkout, name='checkout'),
    path('client-create', views.client_create, name='client-create'),
    path('clients', views.clients, name='clients'),
    path('colors', views.colors, name='colors'),
    path('construction', views.construction, name='construction'),
    path('counters', views.counters, name='counters'),
    path('datatable', views.datatable, name='datatable'),
    path('display', views.display, name='display'),
    path('dropdown', views.dropdown, name='dropdown'),
    path('empty', views.empty, name='empty'),
    path('error400', views.error400, name='error400'),
    path('error404', views.error404, name='error404'),
    path('error500', views.error500, name='error500'),
    path('error501', views.error501, name='error501'),
    path('faq', views.faq, name='faq'),
    path('file-attachments', views.file_attachments, name='file-attachments'),
    path('file-manager-1', views.file_manager_1, name='file-manager-1'),
    path('file-manager-2', views.file_manager_2, name='file-manager-2'),
    path('file-manager', views.file_manager, name='file-manager'),
    path('flex', views.flex, name='flex'),
    path('footers', views.footers, name='footers'),
    path('forgot-password', views.forgot_password, name='forgot-password'),
    path('form-advanced', views.form_advanced, name='form-advanced'),
    path('form-editable', views.form_editable, name='form-editable'),
    path('form-elements', views.form_elements, name='form-elements'),
    path('form-layouts', views.form_layouts, name='form-layouts'),
    path('form-validation', views.form_validation, name='form-validation'),
    path('form-wizard', views.form_wizard, name='form-wizard'),
    path('gallery', views.gallery, name='gallery'),
    path('height', views.height, name='height'),
    path('icons', views.icons, name='icons'),
    path('icons2', views.icons2, name='icons2'),
    path('icons3', views.icons3, name='icons3'),
    path('icons4', views.icons4, name='icons4'),
    path('icons5', views.icons5, name='icons5'),
    path('icons6', views.icons6, name='icons6'),
    path('icons7', views.icons7, name='icons7'),
    path('icons8', views.icons8, name='icons8'),
    path('icons9', views.icons9, name='icons9'),
    path('icons10', views.icons10, name='icons10'),
    path('index', views.index, name='index'),
    #path('invoice-create', views.invoice_create, name='invoice-create'),
    #path('invoice-details', views.invoice_details, name='invoice-details'),
    #path('invoice-edit', views.invoice_edit, name='invoice-edit'),
    #path('invoice-list', views.invoice_list, name='invoice-list'),
    #path('invoice-timelog', views.invoice_timelog, name='invoice-timelog'),
    #path('landing', views.landing, name='landing'),
    #path('loaders', views.loaders, name='loaders'),
    #path('lockscreen', views.lockscreen, name='lockscreen'),
   
    path('mail-compose', views.mail_compose, name='mail-compose'),
    path('mail-inbox', views.mail_inbox, name='mail-inbox'),
    path('mail-read', views.mail_read, name='mail-read'),
    path('mail-settings', views.mail_settings, name='mail-settings'),
    path('maps', views.maps, name='maps'),
    path('maps1', views.maps1, name='maps1'),
    path('maps2', views.maps2, name='maps2'),
    path('margin', views.margin, name='margin'),
    path('mediaobject', views.mediaobject, name='mediaobject'),
    path('modal', views.modal, name='modal'),
    path('navigation', views.navigation, name='navigation'),
    path('notify', views.notify, name='notify'),
    path('offcanvas', views.offcanvas, name='offcanvas'),
    path('opacity', views.opacity, name='opacity'),
    path('padding', views.padding, name='padding'),
    path('pagination', views.pagination, name='pagination'),
    path('panels', views.panels, name='panels'),
    path('position', views.position, name='position'),
    path('pricing', views.pricing, name='pricing'),
    path('product-details', views.product_details, name='product-details'),
    path('products', views.products, name='products'),
    path('profile', views.profile, name='profile'),
    path('progress', views.progress, name='progress'),
    path('project-details/<int:id>/', views.project_details, name='project-details'),
    path('points/<int:parcelle_id>', views.get_points_for_parcelle, name='get_points_for_parcelle'),
    path('get-colors/', views.get_colors, name='get_colors'),
    path('project-edit', views.project_edit, name='project-edit'),
    path('project-new', views.project_new, name='project-new'),
    path('project-new-form', views.project_new_form, name='project-new-form'),
    path('projects-list', views.projects_list, name='projects-list'),
    path('projects', views.projects, name='projects'),
    path('delete-project/<int:project_id>/', views.delete_project, name='delete_project'),
    path('project-modifier/<int:project_id>/', views.project_modifier, name='project-modifier'),
    path('parcelles', views.parcelles, name='parcelles'),
    path('parcelle-details/<int:id>/', views.parcelle_details, name='parcelle-details'),
    path('parcelle-edit', views.parcelle_edit, name='parcelle-edit'),
    path('parcelle-new', views.parcelle_new, name='parcelle-new'),
    path('parcelle-new/<int:id>/', views.parcelle_new_for_project),
    path('parcelles-list', views.parcelles_list, name='parcelles-list'),
    path('parcelle-new-form', views.parcelle_new_form, name='parcelle-new-form'),
    path('rangeslider', views.rangeslider, name='rangeslider'),
    path('rating', views.rating, name='rating'),
    path('register', views.register, name='register'),
    path('scroll', views.scroll, name='scroll'),
    path('services', views.services, name='services'),
    path('settings', views.settings, name='settings'),
    path('sweetalert', views.sweetalert, name='sweetalert'),
    path('switcherpage', views.switcherpage, name='switcherpage'),
    path('table-editable', views.table_editable, name='table-editable'),
    path('tables', views.tables, name='tables'),
    path('tabs', views.tabs, name='tabs'),
    path('tags', views.tags, name='tags'),
    path('task-create', views.task_create, name='task-create'),
    path('task-edit', views.task_edit, name='task-edit'),
    path('tasks-list', views.tasks_list, name='tasks-list'),
    path('terms', views.terms, name='terms'),
    path('thumbnails', views.thumbnails, name='thumbnails'),
    path('ticket-details', views.ticket_details, name='ticket-details'),
    path('timeline', views.timeline, name='timeline'),
    path('tooltipandpopover', views.tooltipandpopover, name='tooltipandpopover'),
    path('treeview', views.treeview, name='treeview'),
    path('typography', views.typography, name='typography'),
    path('users-list', views.users_list, name='users-list'),
    path('width', views.width, name='width'),
    path('wishlist', views.wishlist, name='wishlist'),
    path('wysiwyag', views.wysiwyag, name='wysiwyag'),
    #path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('check_logistiques_access/', check_logistiques_access, name='check_logistiques_access'),
    path('logistiques', views.logistiques, name='logistiques'),
    path('popup/', popup_view, name='popup_view'),
    #path('popup/', views.popup, name='popup'),
    path('logistiques-list', views.logistiques_list, name='logistiques-list'),
    path('machines-engins', views.machines_engins, name='machines-engins'),
    path('outils-agricoles', views.outils_agricoles, name='outils-agricoles'),
    path('infrastructure', views.infrastructure, name='infrastructure'),
    path('fertilisants-traitements', views.fertilisants_traitements, name='fertilisants-traitements'),
    path('graines-pousses', views.graines_pousses, name='graines-pousses'),
    path('carburant', views.carburant, name='carburant'),
    path('pieces-rechange', views.pieces_rechange, name='pieces-rechange'),
    path('rh', views.rh, name='rh'),
    path('reseaux-irrigation', views.reseaux_irrigation, name='reseaux-irrigation'),
    path('reseaux-electrique', views.reseaux_electrique, name='reseaux-electrique'),
    path('poste-transformateur', views.poste_transformateur, name='poste-transformateur'),
    path('panneaux-pv', views.panneaux_pv, name='panneaux-pv'),
    path('generatur', views.generatur, name='generatur'),
    path('moteur', views.moteur, name='moteur'),
    path('securite', views.securite, name='securite'),
    path('batiments', views.batiments, name='batiments'),
    path('maison-villa', views.maison_villa, name='maison-villa'),
    path('hangar-depot', views.hangar_depot, name='hangar-depot'),
    path('local-technique', views.local_technique, name='local-technique'),
    path('frigo', views.frigo, name='frigo'),
    path('engrais', views.engrais, name='engrais'),
    path('traitements', views.traitements, name='traitements'),
    path('autres', views.autres, name='autres'),
    path('meteo', views.meteo, name='meteo'),
    
    path('operations-utilisateur', views.operations_utilisateur, name='operations-utilisateur'),
    path('recommendations-ia', views.recommendations_ia, name='recommendations-ia'),
    path('ajouter-operation-agricole', views.ajouter_operation_agricole, name='ajouter-operation-agricole'),
    
    path('puit', views.puit, name='puit'),
    path('reservoir', views.reservoir, name='reservoir'),
    path('vanne', views.vanne, name='vanne'),
    path('goutte', views.goutte, name='goutte'),
    path('pivot', views.pivot, name='pivot'),
    path('pulverisateur', views.pulverisateur, name='pulverisateur'),
    
    path('analyse', views.analyse, name='analyse'),
    path('get-subcategories/', views.get_subcategories, name='get_subcategories'),
    path('get-anomalies/', views.get_anomalies, name='get_anomalies'),
    path('delete-item/<int:item_id>/', views.delete_item, name='delete_item'),
    path('analyse-details/<int:image_id>/', views.analyse_details, name='analyse-details'),
    path('image_result/', views.analyse, name='image_result'),
    path('upload/', views.analyse, name='upload_image'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)