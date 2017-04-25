---
[![GNU General Public License v3.0](https://raw.github.com/initbrain/btsmapper/master/btsmapper/images/logo_gpl_v3.png)](http://www.gnu.org/licenses/gpl-3.0.txt)  
[GNU General Public License v3.0](http://www.gnu.org/licenses/gpl-3.0.txt)

---

Python Wi-Fi Positioning System
===============================

This script use the Google Geolocation API.  
It was tested on GNU/Linux (require `iw`), OpenBSD (use `ifconfig`) and Mac OS X (require `airport`).  
Special thanks go to contributors!


*   **API key required:**

    A Google API key is required, get it yours here:  
    https://developers.google.com/maps/documentation/geolocation/intro


*   **Screenshot from a previous version (without argparse):**

    ![Python Wi-Fi Positioning System](https://raw.githubusercontent.com/initbrain/Python-Wi-Fi-Positioning-System/master/demo/GNU_Linux_20170108.png)


*   **Installation on GNU/Linux and OpenBSD ($: user, #: root):**

    On GNU/Linux, the script use the `iw` command to gain access to the Wi-Fi peripheral.  
    On OpenBSD, it use the `ifconfig` command to gain access to the Wi-Fi peripheral.  
    On Ubuntu distribution, it require the installation of the following dependencies:

        # apt-get install iw

    On Gentoo distribution, it require the installation of the following dependencies:

        # emerge -av net-wireless/iw

    The full git repository is at: <https://github.com/initbrain/Python-Wi-Fi-Positioning-System>  
    Get it using the following command:

        $ git clone https://github.com/initbrain/Python-Wi-Fi-Positioning-System

    And proceed to final steps.  
    On GNU/Linux, to use the tool, launch it with `root` privileges:

        $ cd Python-Wi-Fi-Positioning-System/
        $ python wifi_positioning_system.py -h
        # python wifi_positioning_system.py --api-key <GOOGLE_API_KEY> -i <WIFI_INTERFACE> --verbose --json-prettify --with-overview --map-type <ROADMAP|SATELLITE|HYBRID|TERRAIN>


*   **Installation on Mac OS X:**

    On Mac OS X, it use `airport` to gain access to the Wi-Fi peripheral.  
    Get it using...

        % TODO

    And proceed to final steps.  

        % python wifi_positioning_system.py --api-key <GOOGLE_API_KEY> --verbose --json-prettify --with-overview --map-type <ROADMAP|SATELLITE|HYBRID|TERRAIN>


*   **Usage:**

    On GNU/Linux and OpenBSD, a Wi-Fi interface name is required to scan with `iw` and `ifconfig` commands:

        usage: wifi_positioning_system.py [-h] [-V] [-L] [-v] [-k API_KEY] [-p] [-o]
                                          [-m {ROADMAP,SATELLITE,HYBRID,TERRAIN}]
                                          (-i WIFI_INTERFACE | --demo)

        optional arguments:
          -h, --help            show this help message and exit
          -V, --version         show program's version number and exit
          -L, --license         show program's license details and exit
          -v, --verbose         enable verbose messages
          -k API_KEY, --api-key API_KEY
                                Google Geolocation API key (could be hardcoded)
          -p, --json-prettify   prettify JSON output
          -o, --with-overview   accuracy overview file generation
          -m {ROADMAP,SATELLITE,HYBRID,TERRAIN}, --map-type {ROADMAP,SATELLITE,HYBRID,TERRAIN}
                                accuracy overview map type

        required arguments:
          -i WIFI_INTERFACE     specify Wi-Fi scan interface
          --demo                demo mode - West Norwood (London)

        additional informations:
          ROADMAP   displays the default road map view
          SATELLITE displays Google Earth satellite images
          HYBRID    displays a mixture of normal and satellite views
                    (this is the default map type)
          TERRAIN   displays a physical map based on terrain information

    On Mac OS X, there is no need of a Wi-Fi interface name to launch a scan with `airport`:

        usage: wifi_positioning_system.py [-h] [-V] [-L] [-v] [-k API_KEY] [-p] [-o]
                                          [-m {ROADMAP,SATELLITE,HYBRID,TERRAIN}]
                                          [--demo]

        optional arguments:
          -h, --help            show this help message and exit
          -V, --version         show program's version number and exit
          -L, --license         show program's license details and exit
          -v, --verbose         enable verbose messages
          -k API_KEY, --api-key API_KEY
                                Google Geolocation API key (could be hardcoded)
          -p, --json-prettify   prettify JSON output
          -o, --with-overview   accuracy overview file generation
          -m {ROADMAP,SATELLITE,HYBRID,TERRAIN}, --map-type {ROADMAP,SATELLITE,HYBRID,TERRAIN}
                                accuracy overview map type
          --demo                demo mode - West Norwood (London)

        additional informations:
          ROADMAP   displays the default road map view
          SATELLITE displays Google Earth satellite images
          HYBRID    displays a mixture of normal and satellite views
                    (this is the default map type)
          TERRAIN   displays a physical map based on terrain information


*   **Contributors (ext-repo):**

    Initial publication on [Twitter](https://twitter.com/initbrain/status/215019236102377472)  
    2012-06-25: modified to run on OS X - [James Armitage (@armitagej)](https://twitter.com/armitagej)  
    2012-06-26: modified to process in python - [Dan Gleebits (@DGleebits)](https://twitter.com/DGleebits)  
    2012-10-01: modified to parse the xml output of airport - [Vincent Ohprecio (@BigsnarfDude)](https://twitter.com/BigsnarfDude)  
    2017-01-03: modified to work with the new Google Geolocation API - [Giovanni Angoli (@juzam)](https://twitter.com/juzam)  
    2017-01-06: merging all modifications - [Julien Deudon (@initbrain)](https://twitter.com/initbrain)  
    2017-01-07: modified to support new permissions assignement methods - [Julien Deudon (@initbrain)](https://twitter.com/initbrain)  
    2017-01-08: source code reorganization - [Julien Deudon (@initbrain)](https://twitter.com/initbrain)  
    2017-01-15: OpenBSD port - [Geoffrey Robert (@mks10110)](https://twitter.com/mks10110)
