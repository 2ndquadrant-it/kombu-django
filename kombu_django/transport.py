"""Kombu transport using the Django database as a message store."""
from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.core import exceptions as errors
from kombu.five import Empty
from kombu.transport import virtual
from kombu.utils import cached_property, symbol_by_name
from kombu.utils.encoding import bytes_to_str
from kombu.utils.json import dumps, loads

VERSION = (1, 0, 0)
__version__ = '.'.join(map(str, VERSION))
POLLING_INTERVAL = getattr(settings, 'KOMBU_POLLING_INTERVAL',
                           getattr(settings, 'DJKOMBU_POLLING_INTERVAL', 5.0))


class Channel(virtual.Channel):
    queue_model = 'kombu_django.models:Queue'

    def _new_queue(self, queue, **kwargs):
        self.Queue.objects.get_or_create(name=queue)

    def _put(self, queue, message, **kwargs):
        self.Queue.objects.publish(queue, dumps(message))

    def basic_consume(self, queue, *args, **kwargs):
        qinfo = self.state.queue_bindings(queue)
        exchange = next(qinfo)
        if self.typeof(exchange).type == 'fanout':
            return
        super(Channel, self).basic_consume(queue, *args, **kwargs)

    def _get(self, queue, timeout=None):
        m = self.Queue.objects.fetch(queue)
        if m:
            return loads(bytes_to_str(m))
        raise Empty()

    def _size(self, queue):
        return self.Queue.objects.size(queue)

    def _purge(self, queue):
        return self.Queue.objects.purge(queue)

    def refresh_connection(self):
        from django import db
        db.connections.close_all()

    @cached_property
    def Queue(self):
        return symbol_by_name(self.queue_model)


class Transport(virtual.Transport):
    Channel = Channel

    default_port = 0
    polling_interval = POLLING_INTERVAL
    channel_errors = (
        virtual.Transport.channel_errors + (
            errors.ObjectDoesNotExist, errors.MultipleObjectsReturned)
    )
    driver_type = 'sql'
    driver_name = 'django'

    def driver_version(self):
        import django
        return '.'.join(map(str, django.VERSION))
