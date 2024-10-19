"""The server module."""

import atexit
from flask import Flask
import structlog

from .constants import ENV_DEVELOPMENT
from .utils import remove_tmp_dir, TMP_DIR
from .config import Config as DefaultConfig, config_by_name as config_name_dict

from .configs.logger.default_json_logger import set_default_logger
from .configs.logger.struct_json_logger import configure_logging


# define the application factory
__all__ = ["create_app"]

# define the default blueprints
DEFAULT_BLUEPRINTS = ()


def create_app(
    config_name: str = "production", app_name: str | None = None, blueprints=None
):
    """Create the Flask app.

    Args:
        config_name (str | None): _description_. the name of the configuration. Defaults to None.
        app_name (str | None, optional): _description_. the name of the app. Defaults to None.
        blueprints (_type_, optional): _description_. the blueprints to configure. Defaults to None.

    Returns:
        _type_: _description_
    """

    # set up app
    if app_name is None:
        app_name = DefaultConfig.PROJECT

    # set up blueprints
    if blueprints is None:
        blueprints = DEFAULT_BLUEPRINTS

    app = Flask(app_name, instance_path=TMP_DIR, instance_relative_config=True)

    configure_app(app, config_name)
    configure_loggers(app)
    configure_hook(app)
    configure_blueprints(app, blueprints)
    configure_error_handlers(app)
    configure_lifecycle_handler(app)

    return app


def configure_loggers(app: Flask):
    """Configure the loggers.

    Args:
        app (Flask): The Flask application.
    """

    set_default_logger(app.config)
    configure_logging(app.config)


def configure_app(app: Flask, config_name: str = ENV_DEVELOPMENT):
    """Configure the Flask app.

    Args:
        app (Flask): The Flask application.
        config_name (str, optional): The name of the configuration. Defaults to ENV_DEVELOPMENT.
    """

    config = config_name_dict[config_name]
    app.config.from_object(config)


def configure_blueprints(app: Flask, blueprints: tuple):
    """Configure blueprints in views.

    Args:
        app (Flask): The Flask application.
        blueprints (tuple): The blueprints to configure.
    """

    for blueprint in blueprints:
        app.register_blueprint(blueprint)


def configure_hook(app: Flask):
    """Configure hooks.

    Args:
        app (Flask): The Flask application.
    """

    @app.before_request
    def before_request():
        structlog.get_logger().info("before_request")


def configure_error_handlers(app: Flask):
    """Configure error handlers.

    Args:
        app (Flask): The Flask application.
    """

    @app.errorhandler(403)
    def forbidden_page(_):
        return "Oops! You don't have permission to access this page.", 403

    @app.errorhandler(404)
    def page_not_found(_):
        return "Opps! Page not found.", 404

    @app.errorhandler(500)
    def server_error_page(_):
        return "Oops! Internal server error. Please try after sometime.", 500


def configure_lifecycle_handler(_: Flask):
    """Configure the lifecycle handler.

    Args:
        app (Flask): The Flask application.
    """
    atexit.register(remove_tmp_dir)
