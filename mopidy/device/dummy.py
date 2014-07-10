"""A dummy device manager for use in tests.

This device manager implements the device manager API in the simplest
way possible.  It is used in tests of the device manager.
"""

from __future__ import unicode_literals

import pykka

from mopidy import device


def create_dummy_device_manager_proxy(config=None):
    return DummyDeviceManager.start().proxy()


class DummyDeviceManager(pykka.ThreadingActor, device.DeviceManager):
    def __init__(self, config, audio):
        super(DummyDeviceManager, self).__init__()
        self.device_types = ['dummy']
        self._devices = set()
        self._connected = set()
        self._paired = set()

    def get_devices(self):
        return map(DummyDeviceManager._make_device, self._devices)

    @staticmethod
    def _make_device(address):
        dev = DummyDevice()
        dev.name = 'dummy_device'
        dev.address = address
        dev.capabilities = [device.DeviceCapability.DEVICE_DUMMY]
        return dev

    def scan(self):
        import string
        import random
        address = ''.join(random.choice(string.ascii_uppercase + string.digits)
                          for _ in range(10))
        self._devices.add(address)

    def connect(self, device):
        if device.address in self._devices:
            self._connected.add(device.address)

    def disconnect(self, device):
        self._connected.discard(device.address)
        self._playing.discard(device.address)

    def pair(self, device):
        if device.address in self._connected:
            self._paired.add(device.address)

    def remove(self, device):
        self._paired.discard(device.address)

    def is_connected(self, device):
        return device.address in self._connected

    def is_paired(self, device):
        return device.address in self._paired

    def set_property(self, device, name, value):
        pass

    def get_property(self, device, name=None):
        if (name is None):
            return device.__dict__
        else:
            return device.__dict__[name]

    def has_property(self, device, name):
        return name in device.__dict__


class DummyDevice(device.Device):
    device_type = 'dummy'
