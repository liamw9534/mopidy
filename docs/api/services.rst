.. _service-api:

***********
Service API
***********

The following requirements both extend and supersede the requirements already stated for implementing
a frontend or backend:

- A service MAY require config values to be set for it to work.

- All config values SHALL be documented.

- All config values MAY be settable in a configuration registry but no error shall be generated if
mandatory config values are missing.

- All config values SHALL also be settable through :meth:`set_property`.  New values shall override
any settings in the configuration registry.

- A service actor SHALL implement a lifecycle in accordance with the following allowed
state transitions:

.. digraph:: service_state_diagram

    None -> Starting
    Starting -> Started, Stopped
    Stopped -> Starting
    Started -> Stopped, Starting

- The 'None' state represents the corner case when the service object has not yet been created or
is in the process of being created.

- The 'Starting' state represents the case when the service is running and may be configured but
is not yet operational owing to missing mandatory configuration parameters.

- The 'Started' state represents the case when the service is running and has all required configuration
values.  The service may also be re-configured during this state, which may result in the service
state changing to 'Starting', as the reconfiguration process takes place.

- The 'Stopped' state represents the case when the service is not running and may not be configured.
The only permissible API call in this state is the start API call. 

- A service's state may be obtained via :meth:`get_service_state`


Service class
=============

.. autoclass:: mopidy.service.Service
    :members:


Service listener
================

.. autoclass:: mopidy.service.ServiceListener
    :members:


Service implementations
=======================

See :ref:`ext-services`.
