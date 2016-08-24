# kodi-remote

## Installation

1. Install python3 (for Debian/Ubuntu users it is as easy as: ```sudo apt-get install python3```)
2. Install pyQt5 for python3 (for Debian/Ubuntu users: ```sudo apt-get install python3-pyqt5```)
3. Download [kodi-remote-master] (https://github.com/chatper/kodi-remote/archive/master.zip) and unzip/extract


## First Use

1. Activate remote control for the kodi instance you want to control (http://kodi.wiki/view/Smart_phone/tablet#Quick_set_up_guide).
2. Access the directory you unziped/extracted (should be 'kodi_remote-master').
3. Use the ```python3 init.py``` command to create a configuration file and follow the instructions.
4. Run the program with the command ```python3 kodi_remote.py```.
5. Press F1 to read about the shortcuts you can use.

## Advanced Usage

You can use ```python3 tcp_remoteGUI.py -i IP_OF_KODI -p PORT``` command, adjusted to your actual values for ip and port of your kodi instance. This will override the values already set by the 'config.ini' file, but only for the current session.
