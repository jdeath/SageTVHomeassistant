# SageTV Support for Homeassistant

I have (poorly) written components for SageTV . There is a media_player as well as a sensor which is compatible with [Lovelace: Upcoming Media Card](https://github.com/custom-cards/upcoming-media-card/). It has been stable for a few days, so probably good enough to share with people. The media_player works well (play/pause/commercial skip) but I cannot get the media_seek function to work. Also, the poster blinks every once in a while.

## Installation

Copy the `sagetv/sensor.py` and `sagetv/media_player.py` to your `custom_components` folder (`custom_components/sagetv/`) in your configuration directory.  If you do not have a `custom_components/sagetv` folder, then you will need to create it.

You must put `ha.js` in your SageTV sagex directory: `C:\Program Files (x86)\SageTV\SageTV\sagex\services\`

Make a posters directory in your local webserver `.homeassistant/www/posters/` to locally cache posters for the upcoming media card

## Configuration
```yaml
sensor:
 - platform: sagetv
    scan_interval: 3600
    sagex: http://192.168.1.2:8080/
    posterdir: "/home/homeassistant/.homeassistant/www/posters/"
    posterurl: https://your.domain.com/local/posters/

media_player:
   - platform: sagetv
     name: Bedroom Sage
     extender: XXXXXXXXXXX
     sagex: "http://192.168.1.X:8080/"   
```

- **sagex**: is the local URL of your sagex API. I assume you can hardcode user/pass, but I do not use one
- **posterdir**: is the directory on your homeassistant system to cache the posters, as my sagex API is not exposed to the internet, but homeassistant is 
- **posterurl**: is the url of the posters directory
- **extender**: is the extender code. Use 0 for a client instance on the server machine. Use the 12 digit code for an extender like an HD200. You can find the code for each of your extenders on the Nielm SageWebserver 

All URLs and Directories must have trailing slash
