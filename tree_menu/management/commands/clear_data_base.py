from django.core.management.base import BaseCommand

from tree_menu.models import TreeMenu, Page


class Command(BaseCommand):
    """ Удаление из базы данных TreeMenu и Page """
    help = "Add test product to the database"

    def handle(self, *args, **kwargs):

        TreeMenu.objects.all().delete()
        Page.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Базы данных TreeMenu и Page удалены"))
