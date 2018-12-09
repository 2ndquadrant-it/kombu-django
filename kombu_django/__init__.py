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

TRANSPORT_CLASS = 'kombu_django.transport:Transport'


def register_transport():
    from kombu import transport
    if 'django' not in transport.TRANSPORT_ALIASES:
        transport.TRANSPORT_ALIASES['django'] = TRANSPORT_CLASS


def unregister_transport():
    from kombu import transport
    if 'django' in transport.TRANSPORT_ALIASES:
        del transport.TRANSPORT_ALIASES['django']
