import requests
import os

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
    if str(resp.status_code)[0] == "4":
        return "URL Error"

    html_url["text"] = resp.text
    html_url["url"] = url

    return html_url
