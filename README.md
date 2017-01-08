---
[![GNU General Public License v3.0](https://raw.github.com/initbrain/btsmapper/master/btsmapper/images/logo_gpl_v3.png)](http://www.gnu.org/licenses/gpl-3.0.txt)  
[GNU General Public License v3.0](http://www.gnu.org/licenses/gpl-3.0.txt)

---

Python Wi-Fi Positioning System
===============================

This script use the Google Maps Geolocation API.  
It was tested on GNU/Linux (require iw) and Mac OS X (require airport).  
Special thanks go to contributors!


*   **API key required:**

    A Google Maps Geolocation API key is required, get it yours here:
    https://developers.google.com/maps/documentation/geolocation/intro


*   **Screenshot:**

    ![Python Wi-Fi Positioning System](https://raw.githubusercontent.com/initbrain/Python-Wi-Fi-Positioning-System/master/demo/GNU_Linux_20170108.png)


*   **Installation on GNU/Linux ($: user, #: root):**

    The script use the 'iw' command to gain access to the Wi-Fi peripheral  
    On Ubuntu distribution, it require the installation of the following dependencies:

        # apt-get install iw

    On Gentoo distribution, it require the installation of the following dependencies:

        # emerge -av net-wireless/iw

    The full git repository is at: <https://github.com/initbrain/Python-Wi-Fi-Positioning-System>  
    Get it using the following command:

        $ git clone https://github.com/initbrain/Python-Wi-Fi-Positioning-System

    And proceed to final steps.  
    On GNU/Linux, to use the tool, launch it with administrator privileges:

        $ cd Python-Wi-Fi-Positioning-System/
        # python wifi_positioning_system.py <wifi interface>


*   **Installation on Mac OS X:**

        $ TODO


*   **Contributors (post-repo):**

    Initial publication on [Twitter](https://twitter.com/initbrain/status/215019236102377472)  
    2012-06-25: modified to run on OS X - [James Armitage (armitagej)](https://twitter.com/armitagej)  
    2012-06-26: modified to process in python - [Dan Gleebits (DGleebits)](https://twitter.com/DGleebits)  
    2012-10-01: modified to parse the xml output of airport - [Vincent Ohprecio (BigsnarfDude)](https://twitter.com/BigsnarfDude)  
    2017-01-03: modified to work with the new Google geolocation API - [Giovanni Angoli (juzam)](https://twitter.com/juzam)  
    2017-01-06: merging all modifications - [Julien Deudon (initbrain)](https://twitter.com/initbrain)  
    2017-01-07: modified to support new permissions assignement methods - [Julien Deudon (initbrain)](https://twitter.com/initbrain)  
    2017-01-08: source code reorganization - [Julien Deudon (initbrain)](https://twitter.com/initbrain)
