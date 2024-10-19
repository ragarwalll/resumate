""" This is the entry point of the application. """

import os
from dotenv import load_dotenv
from server import create_app
from server.constants import ENV_FLASK_CONFIG, ENV_DEVELOPMENT

# load the environment variables
load_dotenv()

# create the application
application = create_app(os.getenv(ENV_FLASK_CONFIG) or ENV_DEVELOPMENT)


@application.cli.command("check")
def initdb():
    """Check the application."""
    print("Application is running.")
