# Download single image
import urllib

def get_img_save(url , filename):
    urllib.urlretrive(url , filename)



from bs4 import BeautifulSoup
import urllib2
import urllib


def make_soup(url):
    query = urllib2.Request(url)
    user_agent = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 1.0.3705)"
    query.add_header("User-Agent" , user_agent)
    html = urllib2.urlopen(query)
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




# Now get images from google custom search for each query
def get_google_img(query):
    image_type ="ActiOn"
    query = query.split()
    query = "+".join(query)
    url = "https://www.google.com/search?q="+query+"tbm=isch"
    print url
    DIR = "./images"

    user_agent = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 1.0.3705)"
    soup = make_soup(url)

    original_images = []
    for img  in soup.find_all("div", {"class" : "rg_meta"}):
        link , Type = json.loads(img.text)["ou"] , json.loads(a.text)["ity"]
        original_images.append((link , Type))

    print "Num images : " + len(original_images)
    
    if not os.path.exists(DIR):
        os.mkdir(DIR)
    DIR = os.path.join(DIR , query.split()[0])

    if not os.path.exists(DIR):
        os.mkdir(DIR)
    
    limit = 10
    count = 0
    for i , (img , Type) in enumerate(original_images):
        if !(count < limit) :
            break
        count += 1

        try:
            req = urllib2.Request(img , headers= {"User-Agent" : user_agent })
            raw_img = urllib2.open(req).read()

            cntr = len([i for i in os.listdir(DIR) if image_type in i]) + 1
            print cntr
            if len(Type) == 0:
                f = open(os.path.join(DIR , "_", image_type , "_" + str(cntr) + ".jpg") , "wb")
            else:
                f = open(os.path.join(DIR , "_" , image_type + "_" + str(cntr) + "." + Type) , "wb")
            
            f.write(raw_img)
            f.close()
        except Exception as e:
            print "could not load : " + img 
            print e


get_google_img("car")
