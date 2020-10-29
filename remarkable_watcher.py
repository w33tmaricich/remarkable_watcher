#!/bin/env python3

import argparse
import time
import logging as log

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

# Setup logging
log.basicConfig(level=log.DEBUG)

# Arguments
parser_description = "Watch a directory and sync with the remarkable"
parser = argparse.ArgumentParser(description=parser_description)
parser.add_argument("--watchdir", help="The directory you want to sync.")
args = parser.parse_args()

# Configuration
patterns = "*"
ignore_patterns = ""
ignore_directories = True
case_sensitive = False

watch_path = args.watchdir
recursive = False


# Event handlers
def on_created(event):
    log.info(f"{event.src_path} created.")


def setup_event_handler():
    event_handler = PatternMatchingEventHandler(patterns, ignore_patterns,
                    ignore_directories, case_sensitive)
    event_handler.on_created = on_created
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
