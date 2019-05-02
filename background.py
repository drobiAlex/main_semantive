from bs4 import BeautifulSoup
from flask import Flask
from celery import Celery
from helpers import get_name, create_dir, download_image, get_html, insert_data

import os


app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'amqp://admin:mypass@rabbit:5672'
app.config['CELERY_RESULT_BACKEND'] = 'rpc://'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


""" Put to the helper program"""

#
# def insert_data(page_name, folder_path, mode):
#     x = mycol.find_one({'webpage': page_name})
#     if mode == "text_path":
#
#         # Insert new data if not exist
#         if x is None:
#             data = {
#                 "webpage": page_name,
#                 "status": "done",
#                 "img_path": "",
#                 "text_path": folder_path,
#             }
#
#             x = mycol.insert_one(data)
#
#             if x:
#                 return "Success"
#         # Update data
#         else:
#             mycol.find_one_and_update(
#                 {"webpage": page_name},
#                 {"$set": {mode: folder_path}})
#             return "Success update"
#
#     elif mode == "img_path":
#         # Insert new data if not exist
#         if x is None:
#             data = {
#                 "webpage": page_name,
#                 "status": "done",
#                 "img_path": folder_path,
#                 "text_path": ""
#             }
#
#             x = mycol.insert_one(data)
#
#             if x:
#                 return "Success"
#         # Update data
#         else:
#             mycol.find_one_and_update(
#                 {"webpage": page_name},
#                 {"$set": {mode: folder_path}})
#             return "Success update"


def parse_img(**kwargs):
    soup = BeautifulSoup(kwargs['text'], features="html.parser")

    images = soup.find_all('img')

    page_name = get_name(kwargs['url'], "")

    # Create a dir
    create_dir(page_name)

    if images:

        f_name = get_name(kwargs['url'], "img_")

        if f_name in os.listdir():
            return "Already exist"

        # Ensure that directory is exist
        create_dir(f_name)

        for i, img in enumerate(images):
            # Call a function to download images
            download_image(i, img)

        folder_path = os.getcwd()

        # Return result of insertion
        feed_back = insert_data(page_name, folder_path, mode="img_path")

        return feed_back

    else:
        return "No images"


def parse_text(**kwargs):
    soup = BeautifulSoup(kwargs["text"], features="html.parser")
    text = ''
    lis = soup.find_all('p')

    for i in lis:
        text += i.text

    # Get a name for folder
    page_name = get_name(kwargs['url'], "")

    # Ensure that folder for web-page is exist. If not - create and go to it
    create_dir(page_name)

    # Get name for a text folder
    text_name = get_name(kwargs['url'], "text_")

    if text_name in os.listdir():
        return "Already exist"

    # Create a dir and change it
    create_dir(text_name)

    with open("text_page.txt", 'w+') as f:
        f.write(text)

    folder_path = os.getcwd()

    # Return result of insertion
    feed_back = insert_data(page_name, folder_path, mode="text_path")

    return feed_back

@celery.task
def save_text(url_link):

    # Request in order to get HTML
    html_url = get_html(url_link)

    # Path to the native dir
    native_dir = os.getcwd()

    feed_back = parse_text(**html_url)

    # Return to the dir of the project
    os.chdir(native_dir)

    return feed_back


@celery.task
def save_img(url_link):

    # Request in order to get HTML
    html_url = get_html(url_link)

    # Path to the native dir
    native_dir = os.getcwd()

    feed_back = parse_img(**html_url)

    # Return to the dir of the project
    os.chdir(native_dir)

    return feed_back
