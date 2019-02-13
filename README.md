# Dreamhost DNS Record Updater

This script allows easy updating of a DNS record on Dreamhost's servers. The original intent of this script is for it to run as a scheduled task on Windows to allow automatic updating of a domain's IP address when the host's public IP changes.

### Requirements

 - Python 3+
 - Python Requests (http://docs.python-requests.org/en/master/)

### Usage
To run the script, edit *config.json* with the necessary information:

| Key | Value |
| ------ | ------ |
| api_key | Generate a Dreamhost API key: https://panel.dreamhost.com/?tree=home.api |
| record | The record you want to update |
| type | The type of record (A, MX, CNAME, TXT, etc.) |
| value | The value (IP) you want to update the record to. Use "public_ip" if you want the record updated to the latest public IP.|

Once *config.json* has been updated, simply run the script:

```sh
python update_dns.py
```

To schedule a task on Windows, visit https://docs.microsoft.com/en-us/windows/desktop/taskschd/task-scheduler-start-page.