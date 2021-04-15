"""
Create permission groups
Create permissions (read only) to models for a set of groups
"""
import logging
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from accounts.models import User

admin=Group.objects.get(name="Admin")
userct = ContentType.objects.get_for_model(User)
view_dashboard = Permission.objects.create(codename ='can_view_dashboard', name ='Can view Dashboard', content_type = userct)

class Command(BaseCommand):

    help = "Creates read only custom permission groups for users"

    def handle(self, *args, **options):
        # dashboard_perm = Permission.objects.get(name='Can view Dashboard')
        # report_perm=Permission.objects.get(name='Can view Report')
        admin.permissions.add(view_dashboard)
        # adm.permissions.add(report_perm)
        