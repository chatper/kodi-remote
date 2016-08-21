import configparser, getpass

config = configparser.ConfigParser()

config['Default'] = {
    'default_ip' : '192.168.10.10',
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
