"""This is a script to update a DNS record hosted on Dreamhost's servers.

This script requires a Dreamhost API key to work.
See README.md for an explanation of the required config file.
"""

import json
import uuid
import requests


def load_config_file(filename):
    """Return dictionary of parameters from config file."""
    try:
        fp = open(filename)
    except IOError:
        print("Error opening file " + filename)
        raise

    try:
        params = json.load(fp)
        return params
    except ValueError:
        print("Config file malformed.")
        raise
    finally:
        fp.close()


def get_public_ip():
    """Return the current public IP from https://ipify.org."""
    r = requests.get('https://api.ipify.org?format=json')
    r.raise_for_status()
    ip_dict = r.json()
    if "ip" in ip_dict:
        return ip_dict["ip"]
    else:
        raise ValueError("Error getting public IP.")


def get_dns_records(params):
    """Return dictionary of all DNS records in Dreamhost account."""
    url = "https://api.dreamhost.com/" + \
          "?key=" + str(params["api_key"]) + \
          "&cmd=dns-list_records" + \
          "&unique_id=" + str(uuid.uuid4()) + \
          "&format=json"
    r = requests.get(url)
    r.raise_for_status()
    records = r.json()
    if "data" in records:
        return records["data"]
    else:
        raise ValueError("Error getting records from Dreamhost.")


def get_record_if_exists(dh_records, params):
    """Checks to see if record specified in config.json exists in current Dreamhost records."""
    for record in dh_records:
        if record["record"] == params["record"] and record["type"] == params["type"]:
            # Return Dreamhost record if record does currently exist.
            return record
    # Return empty dictionary if record does not currently exist on Dreamhost.
    return {}


def remove_record(dh_record, params):
    """Remove the given record from Dreamhost's servers."""
    url = "https://api.dreamhost.com/" + \
          "?key=" + str(params["api_key"]) + \
          "&cmd=dns-remove_record" + \
          "&record=" + str(dh_record["record"]) + \
          "&type=" + str(dh_record["type"]) + \
          "&value=" + str(dh_record["value"]) + \
          "&unique_id=" + str(uuid.uuid4()) + \
          "&format=json"
    r = requests.get(url)
    r.raise_for_status()
    status = r.json()
    if "result" in status:
        if status["result"] != "success":
            raise ValueError("Unsuccessful in removing DNS record from Dreamhost.")
    else:
        raise ValueError("Unknown response from Dreamhost API.")


def add_record(params):
    """Add the given record to Dreamhost's servers."""
    value = get_public_ip() if params["value"] == "public ip" else params["value"]
    url = "https://api.dreamhost.com/" + \
          "?key=" + str(params["api_key"]) + \
          "&cmd=dns-add_record" + \
          "&record=" + str(params["record"]) + \
          "&type=" + str(params["type"]) + \
          "&value=" + str(value) + \
          "&unique_id=" + str(uuid.uuid4()) + \
          "&format=json"
    r = requests.get(url)
    r.raise_for_status()
    status = r.json()
    if "result" in status:
        if status["result"] != "success":
            raise ValueError("Unsuccessful in adding new DNS record to Dreamhost.")
    else:
        raise ValueError("Unknown response from Dreamhost API.")


def main():
    """Update the given DNS record on Dreamhost's servers with the new value.

    If the record already exists, delete the record, and then re-add the record with the new value.
    If the record does not already exist, add the record with the new value.
    """
    params = load_config_file("config.json")
    updated = False

    records = get_dns_records(params)
    record_exists = get_record_if_exists(records, params)
    if record_exists:
        if not (record_exists["value"] == params["value"] and record_exists["type"] == params["type"]):
            remove_record(record_exists, params)
            add_record(params)
            updated = True
    else:
        add_record(params)
        updated = True

    # If record was updated, check that update was successful.
    if updated:
        records = get_dns_records(params)
        success = get_record_if_exists(records, params)
        if success:
            print("Successfully updated DNS record.")
        else:
            print("Failed to update DNS record.")
    else:
        print("DNS record already exists on Dreamhost.")


if __name__ == '__main__':
    main()
