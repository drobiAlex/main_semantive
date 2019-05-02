from bs4 import BeautifulSoup

import pymongo
import requests
import os

# Create a client
myclient = pymongo.MongoClient("mongodb://localhost:27017/")

# Create a databaseО
mydb = myclient["web-loader"]

# Create a collection
mycol = mydb["img_and_text"]

""" Put to the helper program"""


def insert_data(page_name, folder_path, mode):
    x = mycol.find_one({'webpage': page_name})

    print()
    print()
    print()
    print(type(x))  # TO DELETE
    print(type(None))  # TO DELETE
    print()
    print()
    print()

    if mode == "text_path":

        # Insert new data if not exist
        if x is None:
            data = {
                "webpage": page_name,
                "status": "done",
                "img_path": "",
                "text_path": folder_path,
            }

            x = mycol.insert_one(data)

            if x:
                return "Success"
        # Update data
        else:
            mycol.find_one_and_update(
                {"webpage": page_name},
                {"$set": {mode: folder_path}})
            return "Success update"

    elif mode == "img_path":
        # Insert new data if not exist
        if x is None:
            data = {
                "webpage": page_name,
                "status": "done",
                "img_path": folder_path,
                "text_path": ""
            }

            x = mycol.insert_one(data)

            if x:
                return "Success"
        # Update data
        else:
            mycol.find_one_and_update(
                {"webpage": page_name},
                {"$set": {mode: folder_path}})
            return "Success update"


def create_dir(name):
    # Create a folder for a page if not exist
    if name not in os.listdir():
        os.mkdir(name)
    os.chdir(name)


"""Function which change a url of web-page for a proper folder name with type(image or text)"""


def get_name(url, type):
    name = url.split("//")

    if "www" in name[1]:
        name = str(name[1]).replace("www.", "")
        f_name = name.replace("/", " ")
        if f_name[-1] == " ":
            f_name = f_name[:-1]

    else:
        f_name = str(name[1]).replace("/", " ")
        if f_name[-1] == " ":
            f_name = f_name[:-1]

    f_name = type + f_name

    print(f_name)

    return f_name


"""Function which download images"""


def download_image(index, img):
    # Validate that image has a source
    try:
        if img['src'].find("http") == -1:
            print("Not supported")

        else:
            r = requests.get(img['src'])

            if r.status_code == 200:
                name = f"{os.getcwd()}/{index}.jpg"

                with open(name, 'wb') as f:
                    f.write(r.content)
    except:
        print("No url")


def get_html(url):
    html_url = {}

    # Make a request to get a HTML page
    resp = requests.get(url)

    # Ensure that url is ok
    if resp.status_code != 200 or resp.status_code != 302:
        return "URL Error"

    html_url["text"] = resp.text
    html_url["url"] = url

    return html_url


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


def save_text(url_link):

    # Request in order to get HTML
    html_url = get_html(url_link)

    # Path to the native dir
    native_dir = os.getcwd()

    feed_back = parse_text(**html_url)

    # Return to the dir of the project
    os.chdir(native_dir)

    return feed_back


def save_img(url_link):

    # Request in order to get HTML
    html_url = get_html(url_link)

    # Path to the native dir
    native_dir = os.getcwd()

    feed_back = parse_img(**html_url)

    # Return to the dir of the project
    os.chdir(native_dir)

    return feed_back
