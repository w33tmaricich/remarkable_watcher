#!/bin/env python3

import argparse
import time
import logging as log
import subprocess

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

# Setup logging
log.basicConfig(level=log.DEBUG)

# Arguments
parser_description = "watch a directory and sync it with the remarkable locally."
parser = argparse.ArgumentParser(description=parser_description)
parser.add_argument("--ip", help="remarkable ip address.")
parser.add_argument("--username", help="remarkable username.")
parser.add_argument("--password", help="remarkable password.")
parser.add_argument("--watchdir", help="the directory you want to sync.")
args = parser.parse_args()

# Configuration
patterns = "*"
ignore_patterns = ""
ignore_directories = True
case_sensitive = False

watch_path = args.watchdir
recursive = False

remarkable_ip = args.ip
remarkable_user = args.username
remarkable_password = args.password

def file_name_from_path(file_path):
    split_path = file_path.split("/")
    return split_path[-1]


def run_cmd(cmd, success_msg, error_msg):
    try:
        subprocess.run(cmd, shell=True, check=True)
        log.info(success_msg)
    except CalledProcessError:
        log.error(error_msg)


def upload_to_remarkable(file_path):
    file_name = file_name_from_path(file_path)
    cmd = "sshpass -p \"%s\" scp %s %s@%s:/tmp/%s" % (remarkable_password,
          file_path, remarkable_user, remarkable_ip, file_name)
    log.debug(cmd)
    on_success = "Uploaded %s to %s." % (file_name, remarkable_ip)
    on_fail = "Unable to upload %s to your remarkable at %s" % (file_name,
              remarkable_ip)

    run_cmd(cmd, on_success, on_fail)


def remove_from_remarkable(file_path):
    print("TODO: rm -f remote file")


# Event handlers
def on_created(event):
    log.info(f"{event.src_path} created.")
    log.info(f"{event}.")
    upload_to_remarkable(event.src_path)


def on_deleted(event):
    log.info(f"{event.src_path} deleted.")
    log.info(f"{event}.")
    remove_from_remarkable(event.src_path)


def on_modified(event):
    log.info(f"{event.src_path} modified.")
    log.info(f"{event}.")
    upload_to_remarkable(event.src_path)


def on_moved(event):
    log.info(f"{event.src_path} moved.")
    log.info(f"{event}.")


def setup_event_handler():
    event_handler = PatternMatchingEventHandler(patterns, ignore_patterns,
                    ignore_directories, case_sensitive)
    event_handler.on_created = on_created
    event_handler.on_deleted = on_deleted
    event_handler.on_modified = on_modified
    event_handler.on_moved = on_moved
    return event_handler


def setup_observer(path, event_handler):
    observer = Observer()
    observer.schedule(event_handler, path, recursive)
    return observer


def infinate_loop():
    while True:
        time.sleep(20)


def main():

    log.debug("Watching directory: %s" % args.watchdir)
    # Setup
    event_handler = setup_event_handler()
    log.info("Event handler created.")
    observer = setup_observer(watch_path, event_handler)
    log.info("Observer created.")
    observer.start()
    log.info("Observer launched.")

    try:
        infinate_loop()
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
        log.info("Observer stopped.")


if __name__ == "__main__":
    main()
