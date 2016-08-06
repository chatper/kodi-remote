# kodi-remote

## Installation

TODO: Describe the installation process

## Usage

0. Activate remote control for kodi (http://kodi.wiki/view/Smart_phone/tablet#Quick_set_up_guide)
1. Change active directory to /kodi_remote
2. Use 'python3 tcp_remoteGUI.py -i IP_OF_KODI -p PORT' command - if you haven't changed the default settings, port will be 9090.
3. Optional: Edit tcp_remoteGUI.py and change the lines:
    gui.params['ip'] = "DEFAULT_IP_HERE",
    gui.params['port'] = DEFAULT_PORT_HERE,
so that they have useful values. Now you can start the application by using the 'python3 tcp_remoteGUI' command with no arguments.
4. Use your keyboard to interact with kodi.
