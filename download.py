from background import mycol, get_name
from zipfile import ZipFile

import os


def download_file(ulr):
    name = get_name(ulr, "")
    x = mycol.find_one({"webpage": name})
    x = x["text_path"]

    os.chdir(x)
    os.listdir()

    with ZipFile("file.zip", 'w') as myzip:
        myzip.write(os.listdir()[0])

    return os.listdir()[0]
