"""This module contains the configuration classes for the Flask app """

import os


class Config(): # pylint: disable=too-few-public-methods
    """Base configuration class for the Flask app"""

    PROJECT = "resumate"
    PROJECT_NAME = "resumate.backend"
    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True


class ProductionConfig(Config): # pylint: disable=too-few-public-methods
    """Production configuration class for the Flask app"""

    DEBUG = False

class DevelopmentConfig(Config): # pylint: disable=too-few-public-methods
    """Development configuration class for the Flask app"""

    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config): # pylint: disable=too-few-public-methods
    """Testing configuration class for the Flask app"""

    TESTING = True

# Dictionary to map environment names to config classes
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}

# Function to get the config based on environment name
def get_config() -> Config:
    """Function to get the config based on environment name

    Returns:
        Config: The config class based on the environment name
    """
    env = os.getenv('FLASK_ENV', 'development')
    return config_by_name.get(env, Config)
