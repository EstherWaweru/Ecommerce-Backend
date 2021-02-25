from io import StringIO
from django.core.management import call_command
from django.test import TestCase

class CreateGroupTest(TestCase):
    
    def test_command_output(self):
        # args = []
        # opts = GROUPS={ 'Admin':{'log entry': ['add','delete','change','view'],},}
        # out=StringIO()
        # call_command('create_groups',**opts)
        # print(out.getvalue())
        # self.assertIn('Admin',out.getvalue())
        # out = StringIO()
        # call_command('create_groups', stdout=out)
        # self.assertIn('Expected output', out.getvalue())
        pass