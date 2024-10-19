"""Utility functions for the application."""

import os

import tempfile
from shutil import rmtree
import uuid

TMP_DIR_UUID = str(uuid.uuid1())
TMP_DIR = os.path.join(tempfile.gettempdir(), TMP_DIR_UUID)


def create_tmp_dir():
    """Create a temporary directory for the application."""
    os.makedirs(TMP_DIR)


def remove_tmp_dir():
    """Remove the temporary directory for the application."""
    rmtree(TMP_DIR, ignore_errors=True)
