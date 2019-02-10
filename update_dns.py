# This is a script to update a DNS record hosted on Dreamhost's servers.
# This script requires a Dreamhost API key to work.
# See README.md for an explanation of the required config file.

import os
import time
import json
import uuid
import requests


def load_config_file(fp):
    """Load the config file into a dictionary."""
    pass


def get_public_ip():
    """Return the current public IP from https://ipify.org."""
    return 1


def get_current_ip(record, type):
    """Return the IP currently stored in the given DNS record."""
    pass


def delete_record(record, type):
    """Delete the given record from Dreamhost's servers."""
    pass


def add_record(record, type, ip):
    """Add the given record to Dreamhost's servers."""
    pass


def remove_record(record, type, ip):
    """Update the given DNS record on Dreamhost's servers with the new IP.

    If the record already exists, delete the record, and then re-add the record with the new IP.
    If the record does not already exist, add the record with the new IP.
    """
    pass


def main():
    print("hello")


if __name__ == '__main__':
    main()
