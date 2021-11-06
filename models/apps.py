from django import template
from django.apps import AppConfig
from django.db.models.query_utils import RegisterLookupMixin


class ModelsConfig(AppConfig):
    name = 'models'

