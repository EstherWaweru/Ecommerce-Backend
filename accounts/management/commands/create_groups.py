### CREATING GROUPS FOR ECCOMERCE
import logging
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

#dictionary for the groups available

GROUPS={
    'Admin':{
        # general permissions
        'log entry': ['add','delete','change','view'],
        'group': ['add','delete','change','view'],
        'permission': ['add','delete','change','view'],
        'content type': ['add','delete','change','view'],
        'session': ['add','delete','change','view'],
        'user': ['add','delete','change','view']
        # django app model specific permission
    },
    'Customer':{
        #django app model specific permission
        'user': ['delete','change','view']
        #custom permissions


    },
    'DeliveryAgent':{
        #django app model specific permission
        'user': ['delete','change','view']
        #custom permissions

    },
    'Seller':{
        #django app model specific permission
        'user': ['delete','change','view']
        #custom permissions

    }

}
class Command(BaseCommand):
    help="Creates permission for the various available groups"
    def handle(self,*args,**options):
        for group_name in GROUPS:
            new_group,created=Group.objects.get_or_create(name=group_name)
            #loop models in groups
            for app_model in GROUPS[group_name]:
                #loop permissions in grouo
                for permission_name in GROUPS[group_name][app_model]:
                    #generate permission 
                    name = "Can {} {}".format(permission_name,app_model)
                    print("Creating {}".format(name))

                    try:
                        model_add_perm=Permission.objects.get(name=name)
                    except Permission.DoesNotExist:
                        logging.warning("Permission not found with name '{}'.".fromat(name))
                        continue
                    #add permissions to the group
                    new_group.permissions.add(model_add_perm)
