#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Julien Deudon (initbrain) - 20/03/2012
# modified to run on OS X by James Armitage - 25/06/2012
# modified to process in python by Dan Gleebits - 26/06/2012
# modified to parse the xml output of airport by Vincent Ohprecio - 01/10/2012
# modified to work with the new Google geolocation API by Giovanni Angoli (juzam) - 03/01/2017
# merging all modifications by Julien Deudon (initbrain) - 06/01/2017

from commands import getoutput, getstatusoutput
import sys, os, re, simplejson, urllib2


# A Google Maps Geolocation API key is required, get it yours here:
# https://developers.google.com/maps/documentation/geolocation/intro
API_KEY = 'YOUR_KEY'

# TODO check if there is another API from Open Street Map ?


def get_signal_strengths(wifi_scan_method, use_sudo):
    # GNU/Linux
    if wifi_scan_method is 'iw':
        iw_command = '%siw dev %s scan' % ('sudo ' if use_sudo else '', sys.argv[1])
        iw_scan_status, iw_scan_result = getstatusoutput(iw_command)

        if iw_scan_status != 0:
            print "[!] Unable to scan for Wi-Fi networks !"
            print "Used command: '%s'" % iw_command
            print "Result:\n" + '\n'.join(iw_scan_result.split('\n')[:10]) + '\n[...]'
            exit(1)
        else:
            parsing_result = re.compile("BSS ([\w\d\:]+).*\n.*\n.*\n.*\n.*\n\tsignal: ([-\d]+)", re.MULTILINE).findall(iw_scan_result)

            wifi_data = [(bss[0].replace(':', '-'), int(bss[1])) for bss in parsing_result]

    # Mac OS X
    elif wifi_scan_method is 'airport':
        address_match = '([a-fA-F0-9]{1,2}[:|\-]?){6}'  # TODO useless ?
        airport_xml_cmd = '/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport --scan -x'
        airport_scan_status, airport_scan_xml = getstatusoutput(airport_xml_cmd)

        if airport_scan_status != 0:
            print "[!] Unable to scan for Wi-Fi networks !"
            print "Used command: '%s'" % airport_xml_cmd
            print "Result:\n" + '\n'.join(airport_scan_xml.split('\n')[:10]) + '\n[...]'
            exit(1)
        else:
            root = ET.fromstring(airport_scan_xml)
            networks = root.getchildren()[0]

            wifi_data = [(network.find("string").text, abs(int(network.findall("integer")[7].text))) for network in networks]

    return wifi_data


def check_prerequisites():
    if len(sys.argv) < 2:
        print '\nUsage:\n\tpython '+sys.argv[0]+' <wifi interface>\n'
        exit(1)

    # Do something/nothing here for different kind of systems
    if sys.platform in ('linux', 'linux2', 'darwin'):

        wifi_scan_method = None
        use_sudo = False

        # Do something specific to GNU/Linux
        if sys.platform in ('linux', 'linux2'):

            if os.geteuid() != 0:
                which_sudo_status, which_sudo_result = getstatusoutput('which sudo')
                if which_sudo_status != 0:
                    print "\nError: this script need to be run as root !\n"
                    exit(1)
                else:
                    etc_sudoers_status, etc_sudoers_result = getstatusoutput('sudo cat /etc/sudoers')
                    if etc_sudoers_status != 0:
                        print "\nError: this script need to be run as root !\n"
                        exit(1)
                    else:
                        use_sudo = True

            which_iw_status, which_iw_result = getstatusoutput('which iw')
            if which_iw_status != 0:
                print "Missing dependency: 'iw' is needed\n" + \
                      "    iw - tool for configuring Linux wireless devices"
                if 'ubuntu' in getoutput('uname -a').lower():
                    print "    > sudo apt-get install iw"
                # TODO for other distro, see with /etc/*release files ?
                elif 'gentoo' in getoutput('cat /etc/*release').lower():
                    print "    > su -c 'emerge -av net-wireless/iw'"
                exit(1)
            else:
                wifi_scan_method = 'iw'

        # Do something specific to Mac OS X
        elif sys.platform == 'darwin':
            aiport_path = '/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport'
            if not os.path.exists(aiport_path):
                print "Missing dependency:\n" + \
                      "    airport - tool for configuring Apple wireless devices from Terminal.app"
                exit(1)
            else:
                wifi_scan_method = 'airport'
    else:
        # All other systems - or exception for non-supported system
        # Like 'win32'...
        # TODO is 'cygwin' could be found on Mac OS X operation systems ? 
        print "Error: unsupported operating system..." + \
              "\nMicrosoft Windows operating systems are not currently supported, missing Wi-Fi cli tool / library." + \
              "\nIf you use a Mac OS X operating system, the detected plateform could have been 'cygwin'," + \
              "\nplease let us know so we can publish a correction with your help !"
        exit(1)

    return wifi_scan_method, use_sudo


if __name__ == "__main__":
    # TODO argparse

    # Checking permissions, operating system and software dependencies
    wifi_scan_method, use_sudo = check_prerequisites()

    # TODO parameter for displaying messages or not
    print "[+] Scanning nearby Wi-Fi networks..."
    wifi_data = get_signal_strengths(wifi_scan_method, use_sudo)
    
    print "[+] Generating the HTML request"
    location_request = {
        'considerIp': False,
        'wifiAccessPoints':[{
            'macAddress': mac,
            'signalStrength': signal
        } for mac, signal in wifi_data]
    }
    print '\n'.join([l.rstrip() for l in simplejson.dumps(location_request, sort_keys=True, indent=4*' ').splitlines()])
    json_data = simplejson.JSONEncoder().encode(location_request)
    http_request = urllib2.Request('https://www.googleapis.com/geolocation/v1/geolocate?key=' + API_KEY)
    http_request.add_header('Content-Type', 'application/json')

    # Check for missing API_KEY
    if not API_KEY or API_KEY is 'YOUR_KEY':
        print "\nError: a Google Maps Geolocation API key is required, get it yours here:\n" + \
              "https://developers.google.com/maps/documentation/geolocation/intro\n"
        exit(1)

    print "[+] Sending the request to Google"

    # TODO internet connection error handling ?
    api_result = simplejson.loads(urllib2.urlopen(http_request, json_data).read())

    # TODO check if the amount of detected Wi-Fi access points is good enough to call the API
    print "[+] Result"
    print '\n'.join([l.rstrip() for l in simplejson.dumps(api_result, sort_keys=True, indent=4*' ').splitlines()])

    print "[+] Google Maps link"
    print 'https://www.google.com/maps?q=%f,%f' % (api_result['location']['lat'], api_result['location']['lng'])

    # TODO optional parameter
    print "[+] Accuracy overview"

    # TODO parameter for google.maps.MapTypeId
    # ROADMAP   displays the default road map view. This is the default map type.
    # SATELLITE displays Google Earth satellite images
    # HYBRID    displays a mixture of normal and satellite views
    # TERRAIN   displays a physical map based on terrain information.
    map_type = 'HYBRID'  # HYBRID, ROADMAP, SATELLITE, TERRAIN

    html="""<!DOCTYPE html>
    <html>
        <head>
            <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
            <meta http-equiv="content-type" content="text/html; charset=UTF-8"/>

            <style type="text/css">
                html, body {
                    height: 100%;
                    margin: 0;
                    padding: 0;
                }

                #map_canvas {
                    height: 100%;
                }

                @media print {
                    html, body {
                        height: auto;
                    }

                    #map_canvas {
                        height: 650px;
                    }
                }
            </style>

            <title>Geolocation</title>
            <script type="text/javascript" src="http://maps.googleapis.com/maps/api/js?sensor=false"></script>
            <script type="text/javascript">
                function initialize() {
                    var mapOptions = {
                        zoom: 18,
                        center: new
                        google.maps.LatLng("""+str(api_result['location']['lat'])+", "+str(api_result['location']['lng'])+"""),
                        mapTypeId: google.maps.MapTypeId."""+map_type+"""

                    };

                    var map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);

                    // Construct the accuracy circle.
                    var accuracyOptions = {
                        strokeColor: "#000000",
                        strokeOpacity: 0.8,
                        strokeWeight: 2,
                        fillColor: "#000000",
                        fillOpacity: 0.35,
                        map: map,
                        center: mapOptions.center,
                        radius: """+str(api_result["accuracy"])+"""
                    };
                    var accuracyCircle = new google.maps.Circle(accuracyOptions);

                    var contentString = '<div>'+
                        '<p><b>Wi-Fi geolocation</b><br>'+
                        'Latitude : """+str(api_result['location']['lat'])+"""<br>'+
                        'Longitude : """+str(api_result['location']['lng'])+"""<br>'+
                        'Accuracy : """+str(api_result['accuracy'])+"""</p>'+
                        '</div>';

                    var infoWindow = new google.maps.InfoWindow({
                        content: contentString
                    });

                    var marker = new google.maps.Marker({
                        position: mapOptions.center,
                        map: map
                    });

                    google.maps.event.addListener(accuracyCircle, 'click', function() {
                        infoWindow.open(map,marker);
                    });

                    google.maps.event.addListener(marker, 'click', function() {
                        infoWindow.open(map,marker);
                    });
                }
            </script>
        </head>
        <body onload="initialize()">
            <div id="map_canvas"></div>
        </body>
    </html>"""

    # TODO parameters for output file path / name modification
    overview_filename = 'Wifi_geolocation.html'
    with open(overview_filename, 'wb') as overview_file:
        overview_file.write(html)

    pathname = os.path.dirname(sys.argv[0])
    fullpath = os.path.abspath(pathname)
    if not fullpath.endswith('/'):
        fullpath += '/'
    print fullpath + overview_filename
