import urllib.request
import os

def fetch(img_url):
    urllib.request.urlretrieve(img_url, os.path.basename(img_url))

    return os.path.basename(img_url)


