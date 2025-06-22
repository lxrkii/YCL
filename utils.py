import os

DATA_DIR = "diary_entries"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR) 