from __future__ import unicode_literals


class ServiceController(object):
    pykka_traversable = True

    def __init__(self, services, core):
        self.services = services
        self.core = core

    def _get_service_obj(self, service):
        return self.services.services_by_name.get(service)

    def get_services(self):
        return self.services.services_by_name.keys()

    def enable(self, service):
        service_obj = self.services.services_by_name.get(service)
        if (service_obj):
            service_obj.enable()

    def disable(self, service):
        service_obj = self.services.services_by_name.get(service)
        if (service_obj):
            service_obj.disable()

    def is_enabled(self, service):
        return self._service_obj(service).is_enabled().get()

    def set_property(self, service, name, value):
        self._service_obj(service).set_property(service, name, value)

    def get_property(self, service, name=None):
        return self._service_obj(service).get_property(service, name).get()

    def has_property(self, service, name):
        return self._service_obj(service).has_property(service, name).get()
