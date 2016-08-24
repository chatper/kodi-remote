import configparser, getpass
from socket import socket, SOCK_DGRAM, AF_INET 

s = socket(AF_INET, SOCK_DGRAM)
s.connect(('google.com', 0))
yourIP = s.getsockname()[0]
s.close()

ip = input('Enter the IP address of kodi: ')
while not ip[0:ip.rfind('.')] == yourIP[0:yourIP.rfind('.')]:
    print ('The IP address should be something like: %s' % yourIP)
    ip = input('Enter the IP address of kodi: ')

config = configparser.ConfigParser()

config['Default'] = {
    'default_ip' : ip,
    'default_port' : '9090'
}

config['Path'] = {
    'icon_path' : './img/icon.png',
    'img_path' : './img/splash.png',
    'help_img_path' : './img/keyboard.png'
}

config['Other'] = {
    'toast' : getpass.getuser() + ' just connected!'
}

with open('config.ini', 'w') as configfile:
    config.write(configfile)
