from django.core.management.base import BaseCommand
from Praktikum.models import CustomUser
from random import choices
from string import digits

class Command(BaseCommand):
    help = 'Change passwords of all Praktikanten.'
    def handle(self, *args, **options):
        with open("passwords.txt", 'w') as f:
            for User in CustomUser.objects.filter(is_staff=False).order_by('username'):
                pwd = ''.join(choices(digits, k=4))
                out = User.username+' : '+pwd
                f.write(out+'\n')
                print(out)
                User.set_password(pwd)
                User.save()
