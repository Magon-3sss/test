from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
import json

class Command(BaseCommand):
    help = 'Exporte les groupes et les permissions dans un fichier JSON'

    def handle(self, *args, **options):
        data = []
        for group in Group.objects.all():
            group_data = {
                'name': group.name,
                'permissions': [perm.codename for perm in group.permissions.all()]
            }
            data.append(group_data)

        with open('permissions.json', 'w') as json_file:
            json.dump(data, json_file)
