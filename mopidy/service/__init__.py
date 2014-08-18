from __future__ import unicode_literals

from mopidy import listener


class Service(object):
    name = None

    def get_service_name(self):
        """
        Get the service name for this service object.

        :return: service name
        :rtype: string
        """
        return self.name

    def set_property(self, name, value):
        """
        Set a service's property.  For servicess that have
        implementation-specific configuration settings, these may be exposed
        for setting through this method.

        :param name: the property name to set
        :type name: string
        :param value: the value of the property to set
        :type value: implementation-specific to device
        """
        pass

    def get_property(self, name=None):
        """
        Get a service's property.  For servicess that have
        implementation-specific configuration settings, these may be exposed
        for setting through this method.

        :param name: the property name to get, or None to get all properties
        :type name: string
        :return property value or all property values where name is None
        :rtype: dictionary of all properties or implementation-specific property value
        """
        pass

    def has_property(self, name):
        """
        Check if a service has a particular property name.  For services that have
        implementation-specific configuration settings, these may be exposed
        for setting through this method.

        :param name: the property name to check
        :type name: string
        :return True if the property exists, False otherwise
        :rtype: boolean
        """
        pass
        
    def enable(self):
        """
        Enable the service.  Starts enabled by default, so should
        be called following a disable.  Events may be emitted following
        an enable.
        """
        pass

    def disable(self):
        """
        Disable the service.  No events should be emitted following
        a disable.
        """
        pass

    def is_enabled(self):
        """
        Ascertain if the service is enabled.

        :return True if the service is enabled, False otherwise.
        :rtype: boolean
        """
        pass


class ServiceListener(listener.Listener):
    """
    Marker interface for recipients of events sent by service actors.

    Any Pykka actor that mixes in this class will receive calls to the methods
    defined here when the corresponding events happen in the core actor. This
    interface is used both for looking up what actors to notify of the events,
    and for providing default implementations for those listeners that are not
    interested in all events.

    Normally, only the Core actor should mix in this class.
    """

    @staticmethod
    def send(event, **kwargs):
        """Helper to allow calling of service listener events"""
        listener.send_async(ServiceListener, event, **kwargs)

    def service_started(self, service):
        """
        Called whenever a new service has been started by mopidy.

        *MUST* be implemented by actor.

        :param service: the service name that has been started
        :type service: string
        """
        pass

    def service_stopped(self, service):
        """
        Called whenever a service has been stopped by mopidy

        *MAY* be implemented by actor.

        :param service: the service name that has been stopped
        :type service: string
        """
        pass

    def service_property_changed(self, service, props):
        """
        Called whenever a device has been connected to mopidy.

        *MUST* be implemented by actor.

        :param service: the service name that has been stopped
        :type service: string
        :param props: property name/values that have been modified
        :type service: dict
        """
        pass
