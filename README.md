# Remarkable Watcher

Watches a directiory for new files. When files are added, they are uploaded
to the remarkable cloud and removed from the folder.

## Installation
```
pip3 install -r requirements.txt
```

Make sure you have the following installed:
- ssh
- sshpass

## Usage
```
usage: remarkable_watcher.py [-h] [--ip IP] [--username USERNAME]
                             [--password PASSWORD] [--watchdir WATCHDIR]

watch a directory and sync it with the remarkable locally.

optional arguments:
  -h, --help           show this help message and exit.
  --ip IP              remarkable ip address.
  --username USERNAME  remarkable username.
  --password PASSWORD  remarkable password.
  --watchdir WATCHDIR  the directory you want to sync.
```
