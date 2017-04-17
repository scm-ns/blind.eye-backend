# Download single image
import urllib

def get_img_save(url , filename):
    urllib.urlretrive(url , filename)



from bs4 import BeautifulSoup
from urllib2 import urlopen
import urllib


def make_soup(url):
    html = urlopen(url).read()
    return BeautifulSoup(html)

# This gets all the images from the given url and stores in the current directory
# So, now I just need to combine this with another function which goes through
# a list of items, searches for each of them on google images. 

def get_images(url):
    soup = make_soup(url)
    images = [img for img in soup.findAll("img")]
    print( str(len(images)) + " images found.")
    print "Saving images to current dir"
    image_links = [each.get("src") for each in images]
    for each in image_links:
        filename = each.split("/")[-1]
        urllib.urlretrieve(each , filename)
    return image_links
