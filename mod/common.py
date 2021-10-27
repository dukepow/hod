import urllib.request
import mod.UJlib as ujlib
import mimetypes
from urllib.parse import urlparse
import os

mimetypes.init()


# def get_mimetype(file_name='.jpg'):
#     a = urlparse(file_name)
#     fn = os.path.basename(a.path)

#     return mimetypes.types_map[file_name]


def get_mimetype(url):
    """
    Guess based on the file extension.

    Args:
        url (text): Web url that was linked to by a reddit submission.

    Returns:
        modified_url (text): The url (or filename) that will be used when
            constructing the command to run.
        content_type (text): The mime-type that will be used when
            constructing the command to run. If the mime-type is unknown,
            return None and the program will fallback to using the web
            browser.
    """
    filename = url.split('?')[0]
    filename = filename.split('#')[0]
    content_type, encoding = mimetypes.guess_type(filename)
    return url, content_type


def URLDownloadToFile(url, file=None):
    # url = "http://download.thinkbroadband.com/10MB.zip"
    opener = urllib.request.build_opener()

    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]

    urllib.request.install_opener(opener)

    if file is None:
        file_name = url.split('/')[-1]
    else:
        file_name = file
    print("Downloading {}".format(file_name))
    urllib.request.urlretrieve(url, file_name, ujlib.show_progress)


if __name__ == "__main__":
    URLDownloadToFile("http://download.thinkbroadband.com/10MB.zip")
    # URLDownloadToFile("https://velopert.com/wp-content/uploads/2016/05/Feelzgoodman.png")
