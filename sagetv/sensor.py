from homeassistant.const import TEMP_CELSIUS
from homeassistant.helpers.entity import Entity
import requests
import json
import os
import urllib
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from urllib.request import urlretrieve
from requests.utils import requote_uri
from homeassistant.components.media_player import (
    MediaPlayerDevice, PLATFORM_SCHEMA)

CONF_SAGEX = 'sagex'
CONF_POSTERDIR = 'posterdir'
CONF_POSTERURL = 'posterurl'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_SAGEX): cv.string,
    vol.Required(CONF_POSTERDIR): cv.string,
    vol.Required(CONF_POSTERURL): cv.string,
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""
    conf = discovery_info if discovery_info else config
    add_devices([ExampleSensor(conf[CONF_SAGEX],conf[CONF_POSTERDIR],conf[CONF_POSTERURL])])


class ExampleSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self,sagex,posterdir,posterurl):
        """Initialize the sensor."""
        self._state = None
        self._sagex = sagex
        self._posterdir = posterdir;
        self._posterurl = posterurl;
        self.data = None
        self.change_detected = True
        self.update()
    @property
    def name(self):
        """Return the name of the sensor."""
        return 'SageTV'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return 'shows'

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return 'mdi:calendar'

    def update(self):
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = 1
        baseFile = self._posterdir
        baseURL =  self._posterurl
        r = requests.get(self._sagex + 'sagex/api?c=ha:GetNewShows&encoder=json')
        rawJson = r.json();
        aLength = len(rawJson["Result"])
        for x in range(aLength-1):
                title = rawJson["Result"][x+1]["title"]
                origURL = rawJson["Result"][x+1]["poster"]
                origFAURL = rawJson["Result"][x+1]["fanart"]
                title = title.replace("'","-")
                title = title.replace(":","-")
                title = title.replace("&","-")
                rawJson["Result"][x+1]["poster"] = baseURL + title
                rawJson["Result"][x+1]["fanart"] = baseURL + title + '_FA'
                fileName = baseFile + title
                fileNameFA = baseFile + title + '_FA'
                self.change_detected = True
                self._state = len(rawJson["Result"]);
                if not os.path.isfile(fileName):
                        url = requote_uri(origURL)
                        try:
                            urllib.request.urlretrieve(url, fileName)
                        except Exception as e:
                            pass
                if not os.path.isfile(fileNameFA):
                        url = requote_uri(origFAURL)
                        try:
                            urllib.request.urlretrieve(url, fileNameFA)
                        except Exception as e:
                            rawJson["Result"][x+1]["fanart"] = ''
                            pass
                if aLength > 0:
                    rawJson["Result"][0]["title_default"] = rawJson["Result"][0]["titledefault"]
                    rawJson["Result"][0]["line1_default"] = rawJson["Result"][0]["line1default"]
                    rawJson["Result"][0]["line2_default"] = rawJson["Result"][0]["line2default"]
                    rawJson["Result"][0]["line3_default"] = rawJson["Result"][0]["line3default"]
                    rawJson["Result"][0]["line4_default"] = rawJson["Result"][0]["line4default"]
                    
                self.data = json.dumps(rawJson["Result"])

    @property
    def extra_state_attributes(self):
        import math
        attributes = {}
        if self.change_detected:
                attributes['data'] = self.data
                self.change_detected = False
        return attributes
