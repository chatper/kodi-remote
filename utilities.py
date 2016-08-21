import configparser

config = configparser.ConfigParser()
config.read('config.ini')

DEFAULT_IP = config['Default']['default_ip']
DEFAULT_PORT = int(config['Default']['default_port'])
ICON_PATH = config['Path']['icon_path']
IMG_PATH = config['Path']['img_path']
HELP_IMG_PATH = config['Path']['help_img_path']
TOAST = config['Other']['toast']
