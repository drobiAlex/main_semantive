from helpers import mycol, get_name
from zipfile import ZipFile
from background import celery

import os

@celery.task
def download_file(ulr):
    name = get_name(ulr, "")
    x = mycol.find_one({"webpage": name})
    x = x["text_path"]

    os.chdir(x)

    if "afile.zip" not in os.listdir():

        # Create a zip if not exist
        with ZipFile("afile.zip", 'w') as myzip:
            myzip.write(os.listdir()[0])

    return os.listdir()[0]
