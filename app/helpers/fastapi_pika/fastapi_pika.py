# coding=utf-8
import logging

from pika.adapters.blocking_connection import BlockingChannel

from app.core.config import settings

_logger = logging.getLogger(__name__)

import datetime
import pika
from queue import Queue


class Pika(object):
    def __init__(self, app=None):
        """
            Create the Fastapi Pika extension.
        """
        self.app = app
        self.init_app(app)

        self._pika_connection_params = None
        self.pool_size = 1
        self.pool_recycle = -1
        self.pool_queue = Queue()
        self.channel_recycle_times = {}

    def init_app(self, app):
        """
            Initialize the Fastapi Pika extension
        """
        self.app = app
        pool_params = None
        # pool_params = {
        #     'pool_size': 8,           # number of channels to have open at any one time
        #     'pool_recycle': 600       # amount of time in seconds before a channel is closed and it's replaced in
        #                               # the pool (internally this is done on checkout
        # }

        uri = settings.RABBITMQ_URI
        pika_params = pika.URLParameters(uri)
        pika_params.socket_timeout = 5
        self._pika_connection_params = pika_params
        # connection = pika.BlockingConnection(params)

        self._debug("Connection params are %s" % self._pika_connection_params)

        # setup pooling if requested
        if pool_params:
            self.pool_size = pool_params['pool_size']
            self.pool_recycle = pool_params['pool_recycle']
            for i in range(self.pool_size):
                channel = PrePopulationChannel()
                self.__set_recycle_for_channel(channel, -1)
                self.pool_queue.put(channel)
            self._debug("Pool params are %s" % pool_params)

    def __create_channel(self) -> BlockingChannel:
        """
            Create a connection and a channel based on pika params
        """
        pika_connection = pika.BlockingConnection(self._pika_connection_params)
        channel = pika_connection.channel()
        self._debug("Created AMQP Connection and Channel %s" % channel)
        self.__set_recycle_for_channel(channel)
        return channel

    def __destroy_channel(self, channel):
        """
            Destroy a channel by closing it's underlying connection
        """
        self.__remove_recycle_time_for_channel(channel)
        try:
            channel.connection.close()
            self._debug("Destroyed AMQP Connection and Channel %s" % channel)
        except Exception as e:
            self._warn("Failed to destroy channel cleanly %s" % e)

    def __set_recycle_for_channel(self, channel, recycle_time=None):
        """
            Set the next recycle time for a channel
        """
        if recycle_time is None:
            recycle_time = (unix_time_millis_now() + (self.pool_recycle * 1000))

        self.channel_recycle_times[hash(channel)] = recycle_time

    def __remove_recycle_time_for_channel(self, channel):
        """
            Remove the recycle time for a given channel if it exists
        """
        channel_hash = hash(channel)
        if channel_hash in self.channel_recycle_times:
            del self.channel_recycle_times[channel_hash]

    def __should_recycle_channel(self, channel):
        """
            Determine if a channel should be recycled based on it's recycle time
        """
        recycle_time = self.channel_recycle_times[hash(channel)]
        return recycle_time < unix_time_millis_now()

    def channel(self):
        """
            Get a channel
            If pooling is setup, this will block until a channel is available
            If pooling is not setup, a new channel will be created
        """
        # if using pooling
        if self.pool_recycle > -1:
            # get channel from pool or block until channel is available
            ch = self.pool_queue.get()
            self._debug("Got Pika channel from pool %s" % ch)

            # recycle channel if needed or extend recycle time
            if self.__should_recycle_channel(ch):
                old_channel = ch
                self.__destroy_channel(ch)
                ch = self.__create_channel()
                self._debug(
                    "Pika channel is too old, recycling channel %s and replacing it with %s" % (old_channel, ch))
            else:
                self.__set_recycle_for_channel(ch)

            # make sure our channel is still open
            while not ch or not ch.is_open:
                old_channel = ch
                self.__destroy_channel(ch)
                ch = self.__create_channel()
                self._warn("Pika channel not open, replacing channel %s with %s" % (old_channel, ch))

        # if not using pooling
        else:
            # create a new channel
            ch = self.__create_channel()

        # add support context manager
        def close():
            self.return_channel(ch)

        ch = ProxyContextManager(instance=ch, close_callback=close)

        return ch

    def return_channel(self, channel):
        """
            Return a channel
            If pooling is setup, will return the channel to the channel pool
                **unless** the channel is closed, then channel is passed to return_broken_channel
            If pooling is not setup, will destroy the channel
        """
        # if using pooling
        if self.pool_recycle > -1:
            self._debug("Returning Pika channel to pool %s" % channel)
            if channel.is_open:
                self.pool_queue.put(channel)
            else:
                self.return_broken_channel(channel)

        # if not using pooling then just destroy the channel
        else:
            self.__destroy_channel(channel)

    def return_broken_channel(self, channel):
        """
            Return a broken channel
            If pooling is setup, will destroy the broken channel and replace it in the channel pool with a new channel
            If pooling is not setup, will destroy the channel
        """
        # if using pooling
        if self.pool_recycle > -1:
            self._warn("Pika channel returned in broken state, replacing %s" % channel)
            self.__destroy_channel(channel)
            self.pool_queue.put(self.__create_channel())

        # if not using pooling then just destroy the channel
        else:
            self._warn("Pika channel returned in broken state %s" % channel)
            self.__destroy_channel(channel)

    def _debug(self, msg):
        _logger.debug(msg)

    def _warn(self, msg):
        _logger.warning(msg)


class PrePopulationChannel(object):

    def __init__(self):
        self._connection = PrePopulationConnection()

    @property
    def connection(self):
        return self._connection


class PrePopulationConnection(object):

    def __init__(self):
        pass

    def close(self):
        pass


def unix_time(dt):
    """
        Return unix time in microseconds
    """
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return int((delta.microseconds + (delta.seconds + delta.days * 24 * 3600) * 10 ** 6) / 10 ** 6)


def unix_time_millis(dt):
    """
        Return unix time in milliseconds
    """
    return round(unix_time(dt) * 1000.0)


def unix_time_millis_now():
    """
        Return current unix time in milliseconds
    """
    return unix_time_millis(datetime.datetime.utcnow())


class ProxyContextManager(object):
    """
        working as proxy object or as context manager for object
    """

    def __init__(self, instance, close_callback=None):
        self.instance = instance
        self.close_callback = close_callback

    def __getattr__(self, key):
        try:
            return object.__getattribute__(self, key)
        except AttributeError:
            return getattr(self.instance, key)

    def __enter__(self):
        return self.instance

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.close_callback:
            self.close_callback()
        else:
            self.instance.close()
