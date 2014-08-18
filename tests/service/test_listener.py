from __future__ import unicode_literals

import unittest

import mock

from mopidy import service


class ServiceListenerTest(unittest.TestCase):
    def setUp(self):
        self.listener = service.ServiceListener()

    def test_on_event_forwards_to_specific_handler(self):
        self.listener.service_starting = mock.Mock()
        self.listener.service_started = mock.Mock()
        self.listener.service_stopped = mock.Mock()
        self.listener.service_property_changed = mock.Mock()

        self.listener.on_event('service_starting', service='dummy')
        self.listener.service_starting.assert_called_with(service='dummy')
        self.listener.on_event('service_started', service='dummy')
        self.listener.service_started.assert_called_with(service='dummy')
        self.listener.on_event('service_stopped', service='dummy')
        self.listener.service_stopped.assert_called_with(service='dummy')
        self.listener.on_event('service_property_changed', service='dummy', props={'param':1})
        self.listener.service_property_changed.assert_called_with(service='dummy', props={'param':1})

    def test_listener_has_default_impl_for_events(self):
        self.listener.service_starting(service='dummy')
        self.listener.service_started(service='dummy')
        self.listener.service_stopped(service='dummy')
        self.listener.service_property_changed(service='dummy', props={'param':1})
