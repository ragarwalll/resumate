"""This module contains the configuration classes for the Flask app """

import os
from .constants import CONFIG_LOG_LEVEL, ENV_LOG_PRETTY


class Config:  # pylint: disable=too-few-public-methods
    """Base configuration class for the Flask app"""

    PROJECT = "resumate"
    PROJECT_NAME = "resumate.backend"
    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    LOG_LEVEL = os.getenv(CONFIG_LOG_LEVEL, "INFO").upper()
    LOG_PRETTY = os.getenv(ENV_LOG_PRETTY, "False").lower()


class ProductionConfig(Config):  # pylint: disable=too-few-public-methods
    """Production configuration class for the Flask app"""

    DEBUG = False


class DevelopmentConfig(Config):  # pylint: disable=too-few-public-methods
    """Development configuration class for the Flask app"""

    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):  # pylint: disable=too-few-public-methods
    """Testing configuration class for the Flask app"""

    TESTING = True


# Dictionary to map environment names to config classes
config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
