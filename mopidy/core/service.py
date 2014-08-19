from __future__ import unicode_literals


class ServiceController(object):
    pykka_traversable = True

    def __init__(self, services, core):
        self.services = services
        self.core = core

    def _get_service_obj(self, service):
        return self.services.services_by_name.get(service)

    def get_services(self):
        """
        Obtain a list of all named services that are registered

        :return: list of services by service name
        :rtype: list of strings
        """
        return self.services.services_by_name.keys()

    def get_service_state(self, service):
        """
        Get the service state for a named service object.

        :param service: the service name to address
        :type service: string
        :return: service state
        :rtype: string, see :class:`service.ServiceState` for possible values
        """
        return self._get_service_obj(service).get_service_state().get()

    def enable(self, service):
        """
        Enable a disabled service.  This will transition the
        service to the 'Starting' or 'Started' state.

        :param service: the service name to address
        :type service: string
        """
        self._get_service_obj(service).enable()

    def disable(self, service):
        """
        Disable an enabled service.  This will transition the
        service to the 'Stopped' state.

        :param service: the service name to address
        :type service: string
        """
        self._get_service_obj(service).disable()

    def set_property(self, service, name, value):
        """
        Set a named service's property by a property name/value
        pair.  Value may be null in order to clear the setting
        and may result in the service state changing.

        :param service: the service name to address
        :type service: string
        :param name: the property name to set
        :type name: string
        :param value: the value of the property to set
        :type value: implementation-specific to service
        """
        self._get_service_obj(service).set_property(name, value)

    def clear_property(self, service, name):
        """
        Clear a named service's property by property name.
        May result in the service state changing.

        :param service: the service name to address
        :type service: string
        :param name: the property name to set
        :type name: string
        """
        self._get_service_obj(service).clear_property(name)

    def get_property(self, service, name=None):
        """
        Get a service's property value or all property values if the
        property name is set to None.

        :param service: the service name to address
        :type service: string
        :param name: the property name to get, or None to get all properties
        :type name: string
        :return None, property value or all property values where name is None
        :rtype: dictionary of all properties or implementation-specific property value
        """
        return self._get_service_obj(service).get_property(name).get()

    def has_property(self, service, name):
        """
        Check if a service has a particular property name.

        :param service: the service name to address
        :type service: string
        :param name: the property name to check
        :type name: string
        :return True if the property exists, False otherwise
        :rtype: boolean
        """
        return self._get_service_obj(service).has_property(name).get()
