"""
Support for SageTV players.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/SageTV/
"""
from datetime import timedelta
import logging
import requests
import voluptuous as vol

from homeassistant.components.media_player import (
    MediaPlayerDevice, PLATFORM_SCHEMA)
from homeassistant.components.media_player.const import (
    SUPPORT_PAUSE, SUPPORT_PLAY, SUPPORT_STOP,
    SUPPORT_TURN_OFF, SUPPORT_TURN_ON, SUPPORT_NEXT_TRACK, SUPPORT_PREVIOUS_TRACK, SUPPORT_SEEK)
from homeassistant.const import (
    CONF_HOST, CONF_NAME, STATE_IDLE, STATE_OFF, STATE_PLAYING)
import homeassistant.helpers.config_validation as cv
from homeassistant.util.dt import utcnow

REQUIREMENTS = []
CONF_EXTENDER = 'extender'
CONF_SAGEX = 'sagex'
DEFAULT_NAME = "SageTV"
SCAN_INTERVAL = timedelta(seconds=30)

_LOGGER = logging.getLogger(__name__)

SUPPORT_SAGETV = (SUPPORT_PLAY | SUPPORT_STOP | SUPPORT_PAUSE | SUPPORT_NEXT_TRACK | SUPPORT_PREVIOUS_TRACK | SUPPORT_SEEK)
# No host is needed for configuration, however it can be set.
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_SAGEX): cv.string,
    vol.Required(CONF_EXTENDER): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    conf = discovery_info if discovery_info else config

    # Register configured device with Home Assistant.
    add_entities([SageTV( conf[CONF_NAME], conf[CONF_SAGEX], conf[CONF_EXTENDER])])


class SageTV(MediaPlayerDevice):

    def __init__(self, name, sagex, extender):

        # Default name value, only to be overridden by user.
        self._name = name
        self._extender = extender
        self._baseurl = sagex
        # Assume we're off to start with
        self._state = STATE_IDLE
        self._position = 0
        self._duration = 0
        self._position_valid = 0
        self._media_title = ''
        self._title = ''
        self._poster = ''
        self.update()

    @property
    def name(self):
        """Return the display name of this device."""
        return self._name

    @property
    def state(self):
        """Return _state variable, containing the appropriate constant."""
        return self._state

    @property
    def supported_features(self):
        """Flag media player features that are supported."""
        return SUPPORT_SAGETV

    @property
    def media_duration(self):
        """Duration of current playing media in seconds."""
        return self._duration

    @property
    def media_position(self):
        """Position of current playing media in seconds."""
        return self._position

    @property
    def media_position_updated_at(self):
        """When was the position of the current playing media valid."""
        return self._position_valid

    def update(self):
        """Update the internal state by querying the device."""
        # This can take 5+ seconds to complete
        url = self._baseurl + 'sagex/api?c=ha:GetCurrentShow&1=' + self._extender + '&encoder=json'
        r = requests.get(url)
        rawJson = r.json()
        self._state = rawJson["Result"]["isPlaying"]
        if self._state == 'idle':
           self._media_title = ''
           self._poster = ''
           self._duration = 0
           self._position = 0
        else:
           if self._media_title != rawJson["Result"]["title"]:
              self._media_title = rawJson["Result"]["title"]
              self._poster = rawJson["Result"]["poster"]
              self._duration = rawJson["Result"]["duration"]
           self._position = rawJson["Result"]["watchedDuration"]
           self._position_valid = utcnow()

    def media_play(self):
        """Send play command."""
        url = self._baseurl + 'sagex/api?c=ha:Command&1=play&2=' + self._extender
        r = requests.get(url)

    def media_pause(self):
        """Send pause command."""
        url = self._baseurl + 'sagex/api?c=ha:Command&1=pause&2=' + self._extender
        r = requests.get(url)

    def media_stop(self):
        """Send stop command."""
        url = self._baseurl + 'sagex/api?c=ha:Command&1=stop&2=' + self._extender
        r = requests.get(url)

    def media_play_pause(self):
        url = self._baseurl + 'sagex/api?c=ha:PlayPause&1=' +  self._extender
        r = requests.get(url)

    def media_next_track(self):
        url = self._baseurl + 'sagex/api?c=ha:Command&1=Right&2=' +  self._extender
        r = requests.get(url)

    def media_previous_track(self):
        url = self._baseurl + 'sagex/api?c=ha:Command&1=Left&2=' +  self._extender
        r = requests.get(url)

    def async_media_seek(self,position):
        url = self._baseurl + 'sagex/api?c=ha:Seek&1=' +  self._extender + '&2=' + int(position);
        r = requests.get(url)

    @property
    def media_title(self):
        """Title of current playing media."""
        # find a string we can use as a title
        return self._media_title

    @property
    def media_image_url(self):
        return self._poster;
