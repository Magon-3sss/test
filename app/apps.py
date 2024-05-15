from django.apps import AppConfig

class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    def ready(self):
        import app.permissions
        
    """ def ready(self):
        from app.models import MyModel
        MyModel.create_permissions() """ 
    
        
          
        