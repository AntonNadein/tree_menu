from django.urls import path

from tree_menu.apps import TreeMenuConfig
from . import views

app_name = TreeMenuConfig.name

urlpatterns = [
    path("index/", views.Index.as_view(), name="index"),
]
