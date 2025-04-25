from django.urls import path

from tree_menu.apps import TreeMenuConfig
from . import views

app_name = TreeMenuConfig.name

urlpatterns = [
    path("index/", views.Index.as_view(), name="index"),
    path("page/<int:pk>/", views.PageDetail.as_view(), name="page"),
    path("list/", views.ListDetail.as_view(), name="list"),
]
