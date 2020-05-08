import os
import configparser
config = configparser.RawConfigParser()
config.read(['app_config.properties'])

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'in-development'
    
def get_config(section, prop):
    return config.get(section, prop)
