from __future__ import unicode_literals

from mopidy import listener


class Service(object):
    name = None
    """Unique assigned service name string"""
    state = None
    """Service state string - see :class:`.ServiceState` for possible values"""
    public = False
    """Boolean to determine if the inheriting class' API shall be publicly exported.
    Override this if you wish for the API to be fully exported over HTTP/JSON RPC"""

    def get_service_name(self):
        """
        Get the service name for this service object.

        :return: service name
        :rtype: string
        """
        return self.name

    def get_service_state(self):
        """
        Get the service state for this service object.

        :return: service state
        :rtype: string, see :class:`.ServiceState` for possible values
        """
        return self.state

    def set_property(self, name, value):
        """
        Set a service's property.  For services that have
        implementation-specific configuration settings, these may be exposed
        for setting through this method.

        :param name: the property name to set
        :type name: string
        :param value: the value of the property to set
        :type value: implementation-specific to service
        """
        pass

    def clear_property(self, name):
        """
        Clear a service's property value.

        :param name: the property name to clear
        :type name: string
        """
        pass

    def get_property(self, name=None):
        """
        Get a service's property.  For services that have
        implementation-specific configuration settings, these may be exposed
        for setting through this method.  A property that has been
        cleared (or is not yet set) should return a value of None.

        :param name: the property name to get, or None to get all properties
        :type name: string
        :return None, property value or all property values where name is None
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
        Enable the service to transition to 'Starting' state.  Starts enabled by default,
        so should be called following a disable.  Service events may be emitted following
        an enable.
        """
        pass

    def disable(self):
        """
        Disable the service to transition to 'Stopped' state.
        """
        pass


class ServiceListener(listener.Listener):
    """
    Marker interface for recipients of events sent by service actors.

    Any Pykka actor that mixes in this class will receive calls to the methods
    defined here when the corresponding events happen from a given service. This
    interface is used both for looking up what actors to notify of the events,
    and for providing default implementations for those listeners that are not
    interested in all events.
    """

    @staticmethod
    def send(event, **kwargs):
        """Helper to allow calling of service listener events"""
        listener.send_async(ServiceListener, event, **kwargs)

    def service_starting(self, service):
        """
        Called whenever a new service is being started by mopidy and
        is in the process of being configured or re-configured.

        *MUST* be implemented by actor.

        :param service: the service name that is being started
        :type service: string
        """
        pass

    def service_started(self, service):
        """
        Called whenever a new service has been started by mopidy and
        has all required configuration values.

        *MUST* be implemented by actor.

        :param service: the service name that has been started
        :type service: string
        """
        pass

    def service_stopped(self, service):
        """
        Called whenever a service has been stopped by mopidy.

        *MAY* be implemented by actor.

        :param service: the service name that has been stopped
        :type service: string
        """
        pass

    def service_property_changed(self, service, props):
        """
        Called whenever one or more service properties has changed.

        *MUST* be implemented by actor.

        :param service: the service whose property has changed
        :type service: string
        :param props: property name/values that have been modified
        :type service: dict
        """
        pass


class ServiceState(object):
    SERVICE_STATE_STARTING = 'Starting'
    SERVICE_STATE_STARTED = 'Started'
    SERVICE_STATE_STOPPED = 'Stopped'
