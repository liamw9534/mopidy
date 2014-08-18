from __future__ import unicode_literals

from mopidy.service import ServiceListener
from mopidy.service import Service


class DeviceManager(Service):

    def get_devices(self):
        """
        List of all available devices.  This will normally only be
        populated following a device discovery procedure, although some
        technologies may keep their attached devices persistent in a system-wide
        registry.

        :return: a list of `:class:mopidy.models.Device` objects
        :rtype: list
        """
        pass

    def connect(self, device):
        """
        Connect a device.  The interpretation of 'connect' is implementation
        specific.  For example, in bluetooth this may mean connecting the
        device profiles that are compatible with mopidy.  It is intended that
        the 'connected' property is used by other mopidy extension to
        determine whether a device should be used e.g., for audio output.

        :param device: the device to connect.
        :type device: immutable object describing the device uniquely
        """
        pass

    def disconnect(self, device):
        """
        Disconnect a device.  See also `:meth:connect`.

        :param device: the device to disconnect.
        :type device: immutable object describing the device uniquely
        """
        pass

    def pair(self, device):
        """
        Pair a device.  The concept of pairing is required by some device
        technologies as a means to authenticate/permit access to wireless
        devices which may otherwise be attached unintentionally.
        This method should normally be called only after a discovery event
        has been emitted (i.e., device_found) and the device is not yet
        created i.e., `:meth:get_devices()` does not include this device.
        Following a successful pairing, the device_created event should
        be emitted.

        :param device: the device to pair.
        :type device: immutable object describing the device uniquely
        """
        pass

    def remove(self, device):
        """
        Remove a paired device.  The device should be considered no
        longer paired and removed from any system-wide registry.

        :param device: the device to remove.
        :type device: immutable object describing the device uniquely
        """
        pass

    def is_connected(self, device):
        """
        Ascertain if a device is presently connected.

        :param device: the device to check
        :type device: immutable object describing the device uniquely
        """
        pass

    def is_paired(self, device):
        """
        Ascertain if a device is paired.

        :param device: the device to check
        :type device: immutable object describing the device uniquely
        """
        pass

    def set_device_property(self, device, name, value):
        """
        Set a device's property.  For device's that have
        implementation-specific configuration settings, these may be exposed
        for setting through this method.

        :param device: the device whose property to set
        :type device: immutable object describing the device uniquely
        :param name: the property name to set
        :type name: string
        :param value: the value of the property to set
        :type value: implementation-specific to device
        """
        pass

    def get_device_property(self, device, name=None):
        """
        Get a device's property.  For device's that have
        implementation-specific configuration settings, these may be exposed
        for setting through this method.

        :param device: the device whose property to get
        :type device: immutable object describing the device uniquely
        :param name: the property name to get, or None to get all properties
        :type name: string
        :return property value or all property values where name is None
        :rtype: dictionary of all properties or implementation-specific property value
        """
        pass

    def has_device_property(self, device, name):
        """
        Check if a device has a particular property name.  For device's that have
        implementation-specific configuration settings, these may be exposed
        for setting through this method.

        :param device: the device whose property to check
        :type device: immutable object describing the device uniquely
        :param name: the property name to check
        :type name: string
        :return True if the property exists, False otherwise
        :rtype: boolean
        """
        pass


class DeviceListener(ServiceListener):
    """
    Marker interface for recipients of events sent by device manager actors.
    
    Any Pykka actor that mixes in this class will receive calls to the methods
    defined here when the corresponding events happen in the core actor. This
    interface is used both for looking up what actors to notify of the events,
    and for providing default implementations for those listeners that are not
    interested in all events.

    Normally, only the Core actor should mix in this class.
    """

    def device_found(self, device):
        """
        Called whenever a new device has been discovered by a device manager.

        *MUST* be implemented by actor.

        :param device: the device that has been discovered
        :type device: immutable object describing the device's properties
        """
        pass

    def device_disappeared(self, device):
        """
        Called whenever a device is no longer discoverable by a device manager.

        *MAY* be implemented by actor.

        :param device: the device that is no longer discoverable
        :type device: immutable object describing the device's properties
        """
        pass

    def device_connected(self, device):
        """
        Called whenever a device has been connected to mopidy.

        *MUST* be implemented by actor.

        :param device: the device that has been connected
        :type device: immutable object describing the device's properties
        """
        pass

    def device_disconnected(self, device):
        """
        Called whenever a device has been disconnected from mopidy.

        *MUST* be implemented by actor.

        :param device: the device that has been disconnected
        :type device: immutable object describing the device's properties
        """
        pass

    def device_created(self, device):
        """
        Called whenever a new device has been created for the first time.

        *MAY* be implemented by actor.

        :param device: the device that has been created.
        :type device: immutable object describing the device's properties
        """
        pass

    def device_removed(self, device):
        """
        Called whenever a device has been removed.

        *MAY* be implemented by actor.

        :param device: the device that has been removed.
        :type device: immutable object describing the device's properties
        """
        pass

    def device_property_changed(self, device, property_dict):
        """
        Called whenever a device's property changes.

        *MAY* be implemented by actor.

        :param device: the device whose properties have changed
        :type property_dict: properties and values that have changed
        :type device: immutable object describing the device's properties
        :type property_dict: dictionary
        """
        pass

    def device_pin_code_requested(self, device, pin_code):
        """
        Pairing event for devices that are required to input a
        pin code for authentication purposes.  The pin code value will
        be notified to the end user for entry into the device to
        complete the pairing process.

        *MAY* be implemented by actor.

        :param device: the device whose properties have changed
        :type device: immutable object describing the device's properties
        :param pin_code: a sequence of digits describing a PIN
        :type pin_code: string
        """
        pass

    def device_pass_key_confirmation(self, device, pass_key):
        """
        Pairing event for devices that required a self-generated
        pass key to be confirmed by the end user for authentication
        purposes.  The pass key value will notified to the end user
        for comparison against the pass key displayed by the device
        to complete the pairing process.

        *MAY* be implemented by actor.

        :param device: the device whose properties have changed
        :type device: immutable object describing the device's properties
        :param pass_key: a 32-bit number that defines the pass key
        :type pass_key: integer
        """
        pass


class DeviceCapability(object):
    DEVICE_AUDIO_SOURCE = 'AudioSource'
    DEVICE_AUDIO_SINK = 'AudioSink'
    DEVICE_INPUT_CONTROL = 'InputControl'
    DEVICE_DISPLAY = 'Display'
    DEVICE_DUMMY = 'Dummy'
