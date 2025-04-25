from django.contrib import admin

from tree_menu.models import TreeMenu


@admin.register(TreeMenu)
class TreeMenuAdmin(admin.ModelAdmin):
    """ Админ панель для древовидного меню """
    list_display = ('name', 'menu_name', 'parent', 'url', 'named_url',)
    list_filter = ('menu_name',)
    search_fields = ('name', 'menu_name', 'url', 'named_url')
    ordering = ("menu_name",)
    list_display_links = ("name",)
    list_per_page = 20
