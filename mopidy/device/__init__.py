from __future__ import unicode_literals

from mopidy import listener


class DeviceManager(object):
    #: List of strings representing the device type identifier.
    #: This should be set by the device manager itself and normally
    #: represents the subsystem or technology being managed.
    #: For example, 'bluetooth', 'alsa', 'mopidy'.
    device_types = []

    def get_devices(self):
        """
        List of all available devices.  This will normally only be
        populated following a "scan", although some technologies
        may keep their attached devices persistent in a system-wide
        registry e.g., bluetooth - mandatory
        """
        pass

    def enable(self):
        """
        Enable the device manager.  Starts enabled by default, so should
        be called following a disable - mandatory
        """
        pass

    def disable(self):
        """
        Disable the device manager - mandatory
        """
        pass

    def connect(self, device):
        """
        Connect a device - mandatory
        """
        pass

    def disconnect(self, device):
        """
        Disconnect a device - mandatory
        """
        pass

    def pair(self, device):
        """
        Pair a device - optional
        """
        pass

    def remove(self, device):
        """
        Remove a paired device - optional
        """
        pass

    def is_connected(self, device):
        """
        Ascertain if a device is connected - mandatory
        """
        pass

    def is_paired(self, device):
        """
        Ascertain if a device is paired - optional
        """
        pass

    def set_property(self, device, name, value):
        """
        Set a device's property - optional
        """
        pass

    def get_property(self, device, name=None):
        """
        Get a device's property - optional
        """
        pass

    def has_property(self, device, name):
        """
        Check if a device has a particular property name - optional
        """
        pass


class Device(object):
    """
    The Device class defines the following mandatory properties that any
    device must possess and allows a device to be uniquely identified
    by the device manager.  Additional properties may be defined that
    are implementation-specific through sub-classing of this class.
    """

    #: String representing the device type identifier.  This *MUST*
    #: always be set to allow the associated device manager to be
    #: inferred at all times.
    device_type = None

    #: The name *SHOULD* be set to a human-readable device name.
    #: It is not required that the name is unique and name may
    #: be omitted if it is not known.
    name = None

    #: The address *SHALL* be set to an underlying technology physical
    #: address.  The physical address *SHALL* be unique.
    address = None

    #: The capabilities of the device is a list of DeviceCapability
    #: objects which represents specific interactions the device could support
    #: and device properties
    #: See also :class:`mopidy.device.DeviceCapability`
    capabilities = None


class DeviceListener(listener.Listener):
    """
    Marker interface for recipients of events sent by device manager actors.
    
    Any Pykka actor that mixes in this class will receive calls to the methods
    defined here when the corresponding events happen in the core actor. This
    interface is used both for looking up what actors to notify of the events,
    and for providing default implementations for those listeners that are not
    interested in all events.

    Normally, only the Core actor should mix in this class.
    """

    @staticmethod
    def send(event, **kwargs):
        """Helper to allow calling of device manager listener events"""
        listener.send_async(DeviceListener, event, **kwargs)

    def device_found(self, device):
        """
        Called when a device is found.  If the device supports pairing
        and it is not already paired, it may be paired at this point.

        *MAY* be implemented by actor.
        """
        pass

    def device_disappeared(self, device):
        """
        Called when a device disappears.  Pairing no longer possible.

        *MAY* be implemented by actor.
        """
        pass

    def device_connected(self, device):
        """
        Called when a device is connected.

        *MUST* be implemented by actor.
        """
        pass

    def device_disconnected(self, device):
        """
        Called when a device is disconnected.

        *MUST* be implemented by actor.
        """
        pass

    def device_created(self, device):
        """
        Called when a device is created i.e., following pairing.

        *MUST* be implemented by actor.
        """
        pass

    def device_removed(self, device):
        """
        Called when a device is removed i.e., pairing association
        is removed.

        *MAY* be implemented by actor.
        """
        pass

    def device_property_changed(self, device, property_dict):
        """
        Called when a device property changes.

        *MAY* be implemented by actor.
        """
        pass

    def device_pin_code_requested(self, device, pin_code):
        """
        Called when a device pin code is requested during
        pairing.

        *MAY* be implemented by actor.
        """
        pass

    def device_pass_key_confirmation(self, device, pass_key):
        """
        Called when a device pass key requires confirmation
        during pairing.

        *MAY* be implemented by actor.
        """
        pass


class DeviceCapability(object):
    DEVICE_AUDIO_SOURCE = 'AudioSource'
    DEVICE_AUDIO_SINK = 'AudioSink'
    DEVICE_INPUT_CONTROL = 'InputControl'
    DEVICE_DISPLAY = 'Display'
    DEVICE_DUMMY = 'Dummy'
