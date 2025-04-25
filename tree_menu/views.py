from django.views.generic import TemplateView, DetailView, ListView

from tree_menu.models import Page


class Index(TemplateView):
    """Представление домашняя страница"""

    template_name = "tree_menu/index.html"


class PageDetail(DetailView):
    """Представление страниц для проверки """

    model = Page
    template_name = "tree_menu/page_2.html"
    context_object_name = 'page'


class ListDetail(TemplateView):
    """Представление страниц для проверки """

    model = Page
    template_name = "tree_menu/page.html"
    context_object_name = 'page'
