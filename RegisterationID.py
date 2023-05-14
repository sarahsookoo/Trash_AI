"""
Creates a unique registerationID for each raspberry pi
Creates a file that just storees the ID on the Pi.
If no file, create it, otherwise query the file
"""

import os
import uuid

ID_FILE_PATH = "/home/yaya/registerIDFile"

def get_unique_id():
    if not os.path.exists(ID_FILE_PATH):
        id = str(uuid.uuid4())
        with open(ID_FILE_PATH, 'w') as id_file:
            id_file.write(id) # If no file, make it, then return new ID
    else:
        with open(ID_FILE_PATH, 'r') as id_file:
            id = id_file.read().strip() # If file exists, query the ID
    return id

print(get_unique_id())
