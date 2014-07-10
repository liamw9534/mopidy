from __future__ import unicode_literals


class DeviceController(object):
    pykka_traversable = True

    def __init__(self, device_managers, core):
        self.device_managers = device_managers
        self.core = core

    def _device_manager(self, device):
        return self.device_managers.devices_by_type.get(device.device_type)

    def get_devices(self, device_type=None):
        if (device_type):
            device_manager = self.device_managers.devices_by_type.get(device_type)
            if (device_manager):
                return device_manager.get_devices().get()
        else:
            return [device_manager.get_devices().get()
                    for device_manager in self.device_managers.devices_by_type.values()]

    def enable(self, device_type):
        device_manager = self.device_managers.devices_by_type.get(device_type)
        if (device_manager):
            device_manager.enable()

    def disable(self, device_type):
        device_manager = self.device_managers.devices_by_type.get(device_type)
        if (device_manager):
            device_manager.disable()

    def is_connected(self, device):
        self._device_manager(device).is_connect(device).get()

    def is_paired(self, device):
        self._device_manager(device).is_paired(device).get()

    def connect(self, device):
        self._device_manager(device).connect(device)

    def disconnect(self, device):
        self._device_manager(device).disconnect(device)

    def pair(self, device):
        self._device_manager(device).pair(device)

    def remove(self, device):
        self._device_manager(device).remove(device)

    def set_property(self, device, name, value):
        self._device_manager(device).set_property(device, name, value)

    def get_property(self, device, name=None):
        self._device_manager(device).get_property(device, name).get()

    def has_property(self, device, name):
        self._device_manager(device).has_property(device, name).get()
