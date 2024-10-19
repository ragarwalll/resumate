""" This is the entry point of the application. """

from app import create_app

# create the application
application = create_app()


@application.cli.command("check")
def initdb():
    """Check the application."""
    print("Application is running.")
