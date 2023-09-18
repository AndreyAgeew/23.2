import json

from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from skystore.settings import BASE_DIR


class Command(BaseCommand):
    help = 'Создание групп'

    def handle(self, *args, **kwargs):
        Group.objects.all().delete()

        with open(BASE_DIR / 'users/fixtures/groups_fixture.json', 'r', encoding='cp1251') as file:
            group_data = json.load(file)
            for item in group_data:
                group = Group.objects.create(
                    pk=item['pk'],
                    name=item['fields']['name'],
                )
                group.permissions.set(item['fields']['permissions'])
