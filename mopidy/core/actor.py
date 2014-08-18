from __future__ import unicode_literals

import collections
import itertools

import pykka

from mopidy import audio, backend, mixer
from mopidy.audio import PlaybackState
from mopidy.core.service import ServiceController
from mopidy.core.library import LibraryController
from mopidy.core.listener import CoreListener
from mopidy.core.playback import PlaybackController
from mopidy.core.playlists import PlaylistsController
from mopidy.core.tracklist import TracklistController
from mopidy.utils import versioning


class Core(
        pykka.ThreadingActor, audio.AudioListener, backend.BackendListener,
        mixer.MixerListener):

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

    service = None
    """The service controller. An instance of
    :class:`mopidy.core.ServiceController`."""

    def __init__(self, mixer=None, backends=None, services=None, service_classes=None):

        super(Core, self).__init__()

        self.backends = Backends(backends)

        self.services = Services(services, service_classes)

        self.service = ServiceController(services=self.services, core=self)

        self.library = LibraryController(backends=self.backends, core=self)

        self.playback = PlaybackController(
            mixer=mixer, backends=self.backends, core=self)

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

    def state_changed(self, old_state, new_state, target_state):
        # XXX: This is a temporary fix for issue #232 while we wait for a more
        # permanent solution with the implementation of issue #234. When the
        # Spotify play token is lost, the Spotify backend pauses audio
        # playback, but mopidy.core doesn't know this, so we need to update
        # mopidy.core's state to match the actual state in mopidy.audio. If we
        # don't do this, clients will think that we're still playing.

        # We ignore cases when target state is set as this is buffering
        # updates (at least for now) and we need to get #234 fixed...
        if (new_state == PlaybackState.PAUSED and not target_state
                and self.playback.state != PlaybackState.PAUSED):
            self.playback.state = new_state
            self.playback._trigger_track_playback_paused()

    def playlists_loaded(self):
        # Forward event from backend to frontends
        CoreListener.send('playlists_loaded')

    def volume_changed(self, volume):
        # Forward event from mixer to frontends
        CoreListener.send('volume_changed', volume=volume)

    def mute_changed(self, mute):
        # Forward event from mixer to frontends
        CoreListener.send('mute_changed', mute=mute)

    def get_services(self):
        return self.services.services_by_name

    def get_service_classes(self):
        return self.services.classes_by_name


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


class Services(list):
    def __init__(self, services, service_classes):
        super(Services, self).__init__(services)

        self.services_by_name = {}
        self.classes_by_name = {}
        name = lambda b: b.actor_ref.actor_class.__name__

        idx = 0
        for s in services:
            assert s.name.get() not in self.services_by_name, (
                'Cannot add service name %s for %s, '
                'it is already taken by %s'
            ) % (s.name.get(), name(s), name(self.services_by_name[s.name.get()]))
            self.services_by_name[s.name.get()] = s
            self.classes_by_name[s.name.get()] = service_classes[idx]
            idx += 1
