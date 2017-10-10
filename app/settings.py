import os

LISTENER_PORT = int(os.environ.get('LISTENER_PORT'))
TARGET_HOST = os.environ.get('TARGET_HOST')
TARGET_PORT = int(os.environ.get('TARGET_PORT'))
RULES_FILE = os.environ.get('RULES_FILE')
