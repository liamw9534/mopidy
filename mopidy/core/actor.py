from __future__ import unicode_literals

import collections
import itertools

import pykka

from mopidy import audio, backend, device
from mopidy.audio import PlaybackState
from mopidy.core.device import DeviceController
from mopidy.core.library import LibraryController
from mopidy.core.listener import CoreListener
from mopidy.core.playback import PlaybackController
from mopidy.core.playlists import PlaylistsController
from mopidy.core.tracklist import TracklistController
from mopidy.utils import versioning


class Core(pykka.ThreadingActor, audio.AudioListener, backend.BackendListener,
           device.DeviceListener):
    library = None
    """The library controller. An instance of
    :class:`mopidy.core.LibraryController`."""

    playback = None
    """The playback controller. An instance of
    :class:`mopidy.core.PlaybackController`."""

    playlists = None
    """The playlists controller. An instance of
    :class:`mopidy.core.PlaylistsController`."""

    tracklist = None
    """The tracklist controller. An instance of
    :class:`mopidy.core.TracklistController`."""

    def __init__(self, audio=None, backends=None, device_managers=None):
        super(Core, self).__init__()

        self.backends = Backends(backends)

        self.device_managers = Devices(device_managers)

        self.device = DeviceController(device_managers=self.device_managers, core=self)

        self.library = LibraryController(backends=self.backends, core=self)

        self.playback = PlaybackController(
            audio=audio, backends=self.backends, core=self)

        self.playlists = PlaylistsController(
            backends=self.backends, core=self)

        self.tracklist = TracklistController(core=self)
        

    def get_uri_schemes(self):
        futures = [b.uri_schemes for b in self.backends]
        results = pykka.get_all(futures)
        uri_schemes = itertools.chain(*results)
        return sorted(uri_schemes)

    uri_schemes = property(get_uri_schemes)
    """List of URI schemes we can handle"""

    def get_version(self):
        return versioning.get_version()

    version = property(get_version)
    """Version of the Mopidy core API"""

    def reached_end_of_stream(self):
        self.playback.on_end_of_track()

    def state_changed(self, old_state, new_state):
        # XXX: This is a temporary fix for issue #232 while we wait for a more
        # permanent solution with the implementation of issue #234. When the
        # Spotify play token is lost, the Spotify backend pauses audio
        # playback, but mopidy.core doesn't know this, so we need to update
        # mopidy.core's state to match the actual state in mopidy.audio. If we
        # don't do this, clients will think that we're still playing.
        if (new_state == PlaybackState.PAUSED
                and self.playback.state != PlaybackState.PAUSED):
            self.playback.state = new_state
            self.playback._trigger_track_playback_paused()

    def playlists_loaded(self):
        # Forward event from backend to frontends
        CoreListener.send('playlists_loaded')

    def device_found(self, device):
        # Forward event from device to other extensions
        CoreListener.send('device_found', device=device)

    def device_disappeared(self, device):
        # Forward event from device to other extensions
        CoreListener.send('device_disappeared', device=device)

    def device_connected(self, device):
        # Forward event from device to other extensions
        CoreListener.send('device_connected', device=device)

    def device_disconnected(self, device):
        # Forward event from device to other extensions
        CoreListener.send('device_disconnected', device=device)

    def device_created(self, device):
        # Forward event from device to other extensions
        CoreListener.send('device_created', device=device)

    def device_removed(self, device):
        # Forward event from device to other extensions
        CoreListener.send('device_removed', device=device)

    def device_property_changed(self, device, property_dict):
        # Forward event from device to other extensions
        CoreListener.send('device_property_changed', device=device,
                          property_dict=property_dict)

    def device_pin_code_requested(self, device, pin_code):
        # Forward event from device to other extensions
        CoreListener.send('device_pin_code_requested', device=device,
                          pin_code=pin_code)

    def device_pass_key_confirmation(self, device, pass_key):
        # Forward event from device to other extensions
        CoreListener.send('device_pass_key_confirmation', device=device,
                          pass_key=pass_key)


class Backends(list):
    def __init__(self, backends):
        super(Backends, self).__init__(backends)

        self.with_library = collections.OrderedDict()
        self.with_library_browse = collections.OrderedDict()
        self.with_playback = collections.OrderedDict()
        self.with_playlists = collections.OrderedDict()

        backends_by_scheme = {}
        name = lambda b: b.actor_ref.actor_class.__name__

        for b in backends:
            has_library = b.has_library().get()
            has_library_browse = b.has_library_browse().get()
            has_playback = b.has_playback().get()
            has_playlists = b.has_playlists().get()

            for scheme in b.uri_schemes.get():
                assert scheme not in backends_by_scheme, (
                    'Cannot add URI scheme %s for %s, '
                    'it is already handled by %s'
                ) % (scheme, name(b), name(backends_by_scheme[scheme]))
                backends_by_scheme[scheme] = b

                if has_library:
                    self.with_library[scheme] = b
                if has_library_browse:
                    self.with_library_browse[scheme] = b
                if has_playback:
                    self.with_playback[scheme] = b
                if has_playlists:
                    self.with_playlists[scheme] = b


class Devices(list):
    def __init__(self, device_managers):
        super(Devices, self).__init__(device_managers)

        self.devices_by_type = {}
        name = lambda b: b.actor_ref.actor_class.__name__

        for d in device_managers:
            for device_type in d.device_types.get():
                assert device_type not in self.devices_by_type, (
                    'Cannot add device type %s for %s, '
                    'it is already handled by %s'
                ) % (device_type, name(d), name(self.devices_by_type[device_type]))
                self.devices_by_type[device_type] = d
