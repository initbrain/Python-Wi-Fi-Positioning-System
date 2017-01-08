#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Julien Deudon (initbrain) - 20/03/2012
# modified to run on OS X - James Armitage - 25/06/2012
# modified to process in python - Dan Gleebits - 26/06/2012
# modified to parse the xml output of airport - Vincent Ohprecio - 01/10/2012
# modified to work with the new Google geolocation API - Giovanni Angoli (juzam) - 03/01/2017
# merging all modifications - Julien Deudon (initbrain) - 06/01/2017
# modified to support new permissions assignement methods - Julien Deudon (initbrain) - 07/01/2017
# source code reorganisation - Julien Deudon (initbrain) - 08/01/2017


from commands import getoutput, getstatusoutput
import sys, os, grp, re, simplejson, urllib2

# A Google Maps Geolocation API key is required, get it yours here:
# https://developers.google.com/maps/documentation/geolocation/intro
API_KEY = 'YOUR_KEY'

# Alexander Mylnikov API
# https://www.mylnikov.org/archives/1170
# Too many gateway time-out (HTTP error 504)

# TODO support the WiGLE API
# https://wigle.net/

# TODO check the cool display of iSniff-GPS
# https://raw.githubusercontent.com/hubert3/iSniff-GPS/master/iSniff_GPS_Apple_WLOC_screenshot.jpg

# TODO check http://www.minigps.net/cellsearch.html
# TODO check if there is another API from Open Street Map ?


def get_scriptpath():
    pathname = os.path.dirname(sys.argv[0])
    fullpath = os.path.abspath(pathname)

    if not fullpath.endswith('/'):
        fullpath += '/'

    return fullpath


def prettify_json(json_data):
    return '\n'.join([l.rstrip() for l in simplejson.dumps(json_data, sort_keys=True, indent=4*' ').splitlines()])


def create_overview(api_result, filename='Wifi_geolocation.html', filepath=get_scriptpath()):
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
    with open(filepath+filename, 'wb') as overview:
        overview.write(html)
    print filepath + filename

    # Keep the owners
    scriptpath = get_scriptpath()
    script_uid = os.stat(scriptpath+sys.argv[0]).st_uid
    script_gid = os.stat(scriptpath+sys.argv[0]).st_gid
    overview_uid = os.stat(filepath+filename).st_uid
    overview_gid = os.stat(filepath+filename).st_gid
    if overview_uid != script_uid or overview_gid != script_gid:
        os.chown(filepath+filename, script_uid, script_gid)


def get_signal_strengths(wifi_scan_method):
    # GNU/Linux
    if wifi_scan_method is 'iw':
        iw_command = 'iw dev %s scan' % (sys.argv[1])
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
        print 'Python Wi-Fi Positioning System\n\n' + \
              'Usage:\n\tpython '+sys.argv[0]+' <wifi interface>'
        exit(1)

    # Do something/nothing here for different kind of systems
    if sys.platform in ('linux', 'linux2', 'darwin'):
        wifi_scan_method = None
        perm_cmd = None

        # Do something specific to GNU/Linux
        if sys.platform in ('linux', 'linux2'):
            # If not launched with root permissions
            if os.geteuid() != 0:
                # First try with 'sudo'
                which_sudo_status, which_sudo_result = getstatusoutput('which sudo')
                # If 'sudo' is installed and current user in 'sudo' group
                if which_sudo_status is 0:
                    # Like in the ubuntu default sudo configuration
                    # "Members of the admin group may gain root privileges"
                    # "Allow members of group sudo to execute any command"
                    current_user_groups = [grp.getgrgid(g).gr_name for g in os.getgroups()]
                    if 'sudo' in current_user_groups or \
                       'admin' in current_user_groups:
                        perm_cmd = 'sudo'
                    #etc_sudoers_status, etc_sudoers_result = getstatusoutput('sudo cat /etc/sudoers')
                    # If 'sudo' is configured for the current user
                    #if etc_sudoers_status is 0:
                        #perm_cmd = 'sudo'
                # If not 'sudo'
                if perm_cmd is None:
                    # Check other methods for getting permissions
                    for su_gui_cmd in ['gksu', 'kdesu', 'ktsuss', 'beesu', 'su -c', '']:
                        which_cmd_status, which_cmd_result = getstatusoutput('which '+su_gui_cmd.split()[0])
                        # If one is found, keep it in 'su_gui_cmd' var
                        if which_cmd_status is 0:
                            break
                    # If 'su_gui_cmd' var is not empty, we have one !
                    if su_gui_cmd:
                        perm_cmd = su_gui_cmd
                    else:
                        print "Error: this script need to be run as root !"
                        exit(1)
            #else:
                #print "[+] Current user is '%s'" % os.environ.get('USER')

            # Command available to ask permissions
            if perm_cmd:
                # Restart as root
                #print "[+] This script need to be run as root, current user is '%s'" % os.environ.get('USER')
                print "[+] Using '" + perm_cmd.split()[0] + "' for asking permissions"
                #print (perm_cmd.split()[0], perm_cmd.split() + [' '.join(['python'] + sys.argv)])
                os.execvp(perm_cmd.split()[0], perm_cmd.split() + [' '.join(['python'] + sys.argv)])

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

    return wifi_scan_method


if __name__ == "__main__":
    # TODO argparse

    # TODO parameter for demo mode
    demo = False  # Demonstration ?
    if demo:
        # TODO parameter for displaying messages or not
        print "[+] Scanning nearby Wi-Fi networks..."

        # Demo - West Norwood (London)
        print "[+] Generating the HTML request"
        wifi_data = [
            ('00-fe-f4-25-ee-30', -40),
            ('02-fe-f4-25-ee-30', -44),
            ('12-fe-f4-25-ee-30', -44),
            ('00-26-5a-7e-0d-02', -60),
            ('90-01-3b-30-04-29', -60),
            ('2c-b0-5d-bd-db-4a', -50)
        ]
    else:
        # Checking permissions, operating system and software dependencies
        wifi_scan_method = check_prerequisites()

        print "[+] Scanning nearby Wi-Fi networks..."
        wifi_data = get_signal_strengths(wifi_scan_method)
        # TODO check if the amount of detected Wi-Fi access points is good enough to call the API
        
    print "[+] Generating the HTML request"
    location_request = {
        'considerIp': False,
        'wifiAccessPoints':[
            {
                "macAddress": mac,
                "signalStrength": signal
            } for mac, signal in wifi_data]
    }

    print prettify_json(location_request)

    # Check for missing API_KEY
    if not API_KEY or API_KEY is 'YOUR_KEY':
        print "Error: a Google Maps Geolocation API key is required, get it yours here:\n" + \
              "https://developers.google.com/maps/documentation/geolocation/intro"
        exit(1)
    else:
        json_data = simplejson.JSONEncoder().encode(location_request)
        http_request = urllib2.Request('https://www.googleapis.com/geolocation/v1/geolocate?key=' + API_KEY)
        http_request.add_header('Content-Type', 'application/json')

        print "[+] Sending the request to Google"
        # TODO internet connection error handling ?
        api_result = simplejson.loads(urllib2.urlopen(http_request, json_data).read())

        print "[+] Result"
        print prettify_json(api_result)

        print "[+] Google Maps link"
        print 'https://www.google.com/maps?q=%f,%f' % (api_result['location']['lat'], api_result['location']['lng'])

        # TODO optional parameter
        print "[+] Accuracy overview"
        create_overview(api_result)
