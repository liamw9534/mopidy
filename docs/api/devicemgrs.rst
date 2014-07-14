.. _devman-api:

*****************
DeviceManager API
*****************

.. module:: mopidy.device
    :synopsis: The API implemented by device managers

The device manager API is the interface that must be implemented when you create a
device manager. If you are working on an extension and need to access a device manager, see
the :ref:`core-api` instead.


Devices and routing of requests to the device manager
=====================================================

When Mopidy's core layer is processing a client request, it routes the request
to one or more appropriate device managers based on the device objects the
request touches on. All device objects have a device type and device address which,
when combined, form a unique reference.  The device objects' device_type is compared
with the device manager's :attr:`~mopidy.backend.Backend.device_types` to select the
relevant device manager.


DeviceManager class
===================

.. autoclass:: mopidy.device.DeviceManager
    :members:


DeviceManager listener
======================

.. autoclass:: mopidy.device.DeviceManagerListener
    :members:


.. _devman-implementations:

Device manager implementations
==============================

- `Mopidy-BTManager <https://github.com/liamw9534/mopidy-btmanager>`_
