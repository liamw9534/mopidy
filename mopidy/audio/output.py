from __future__ import unicode_literals

import logging

import pygst
pygst.require('0.10')
import gst  # noqa

logger = logging.getLogger(__name__)


class AudioOutput(gst.Bin):
    """
    AudioOutput provides a gst.Bin container for teeing one or more
    audio sink entities which may be dynamically added or removed
    from the container.
    """
    def __init__(self):
        logger.info('Starting audio output "tee"...')
        super(AudioOutput, self).__init__()
        self.tee = gst.element_factory_make("tee")
        self._bins = {}
        self.add(self.tee)
        self.sinkpad = self.tee.get_pad("sink")
        # Add a fakesink by default to avoid the pipeline stalling
        # if no sinks are added
        self.add_sink('_fakesink', FakeAudioSink())
        ghost_pad = gst.GhostPad("sink", self.sinkpad)
        self.add_pad(ghost_pad)

    def _is_running(self):
        """
        Helper function to ascertain if the pipeline is running

        :rtype: boolean
        """
        state = self.get_state()
        return state[1] == gst.STATE_PLAYING

    def add_sink(self, ident, sink_obj):
        """
        Add a new sink device to the tee bin - it is the caller's
        responsibility to ensure that the sink_obj is good and
        can be dynamically inserted.

        :param ident: Unique identifier which will be used as an opaque
            reference to the sink_obj
        :type ident: opaque any type which may be referenced in a
            python dictionary
        :param sink_obj: a gstreamer object which implements the audio sink
        :type gst.Bin or derivative of gst.BaseSink
        """
        
        if (ident in self._bins.keys()):
            raise Exception('Sink object ident = ' + ident + ' is already registered')

        # Remove fakesink if it is inside the bin already
        remove_fakesink = '_fakesink' in self._bins.keys()

        # If Safely add the sink object into the tee gst.Bin object
        self._bins[ident] = {}
        # If the pipeline is running, we must block the sink pad
        # whilst we add the new gst.Bin to the tee
        peer = self.sinkpad.get_peer()
        if (self._is_running() and peer):
            peer.set_blocked(True)
        # Stitch in the new gst.Bin
        sinkpad = sink_obj.get_static_pad('sink')
        srcpad = self.tee.get_request_pad('src%d')
        self.add(sink_obj)
        # Get the new element into the same running state as its
        # new parent gst.Bin to avoid stalling the pipeline
        sink_obj.sync_state_with_parent()
        srcpad.link(sinkpad)
        # Unblock the pad now we've inserted the new gst.Bin
        if (peer):
            peer.set_blocked(False)
        # Register the sink object and its src pad
        self._bins[ident]['sink_obj'] = sink_obj
        self._bins[ident]['srcpad'] = srcpad

        # Remove fakesink if it was already inside
        if (remove_fakesink):
            self.remove_sink('_fakesink')

    def remove_sink(self, ident):
        """
        Remove an existing sink from the tee bin by its unique
        identifier.
        
        :param ident: Unique identifier used as an opaque
            reference to a sink_obj
        :type ident: opaque any type which may be referenced in a
            python dictionary
        """
        # If this is the last bin, we should add fakesink back first
        if (len(self._bins.keys()) == 1):
            self.add_sink('_fakesink', FakeAudioSink())

        if (ident in self._bins.keys()):
            sink = self._bins.pop(ident)
            if (sink is None):
                raise Exception('Unrecognized sink object ident = ' + ident)
            sink_obj = sink['sink_obj']
            srcpad = sink['srcpad']
            # Safely remove the element from the tee gst.Bin
            sinkpad = sink_obj.get_static_pad('sink')
            if (self._is_running()):
                sinkpad.set_blocked(True)
            srcpad.unlink(sinkpad)
            self.tee.release_request_pad(srcpad)
            self.remove(sink_obj)
            sink_obj.set_state(gst.STATE_NULL)


class FakeAudioSink(gst.Bin):
    def __init__(self):
        super(FakeAudioSink, self).__init__()
        queue = gst.element_factory_make('queue')
        fakesink = gst.element_factory_make('fakesink')
        fakesink.set_property('async', True)
        fakesink.set_property('sync', True)
        self.add_many(queue, fakesink)
        gst.element_link_many(queue, fakesink)
        pad = queue.get_pad('sink')
        ghost_pad = gst.GhostPad('sink', pad)
        self.add_pad(ghost_pad)
