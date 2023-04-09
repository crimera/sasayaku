import pycurl
import os
import urllib.parse


def download(url):
    # Create a Curl object
    c = pycurl.Curl()
    # Set the URL of the file to download
    c.setopt(c.URL, url)
    # get the filename
    effective_url = c.getinfo(pycurl.EFFECTIVE_URL)
    filename = urllib.parse.unquote(os.path.basename(effective_url))

    # Set the name of the output file
    with open(filename, 'wb') as f:
        # Write the downloaded data to the file
        c.setopt(c.WRITEDATA, f)
        # Perform the request
        c.perform()
        # Close the Curl object
        c.close()
    return filename
