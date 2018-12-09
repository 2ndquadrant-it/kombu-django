from __future__ import absolute_import, unicode_literals

from . import transport

from kombu_django import register_transport

register_transport()


class test_django(transport.TransportCase):
    transport = 'django'
    prefix = 'django'
    event_loop_max = 10

    def before_connect(self):
        from django.conf import settings
        if not settings.configured:
            settings.configure(
                DATABASE_ENGINE='sqlite3',
                DATABASE_NAME=':memory:',
                DATABASES={
                    'default': {
                        'ENGINE': 'django.db.backends.sqlite3',
                        'NAME': ':memory:',
                    },
                },
                INSTALLED_APPS=('kombu_django',),
            )
        from django import setup, VERSION
        setup()
        from django.core.management import call_command
        if VERSION > (1, 8):
            call_command('makemigrations')
            call_command('migrate')
        else:
            call_command('syncdb')
