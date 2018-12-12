"""Kombu transport using the Django database as a message store."""
from __future__ import absolute_import, unicode_literals

try:
    from django.apps import AppConfig
except ImportError:  # pragma: no cover
    pass
else:
    class KombuAppConfig(AppConfig):
        name = 'kombu_django'
        label = name.replace('.', '_')
        verbose_name = 'Message queue'
    default_app_config = 'kombu_django.KombuAppConfig'
