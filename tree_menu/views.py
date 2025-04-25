from django.views.generic import TemplateView


class Index(TemplateView):
    """Представление домашняя страница"""

    template_name = "tree_menu/index.html"
