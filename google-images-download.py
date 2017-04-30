#Searching and Downloading Google Images/Image Links

#The MIT License (MIT)
#Copyright (c) 2015 Hardick Vasa
#scm-ns 2017 : I just added the ability to store different seach term images by directory

#Import Libraries

import time       #Importing the time library to check the time of code execution
import sys    #Importing the System Library

import urllib2
import os
import multiprocessing
from urllib2 import Request,urlopen
from urllib2 import URLError, HTTPError

import threading


search_keyword = ["dog"]

#search_keyword = [ "dog" , "cat" , "clock" , "shelf" , "pan" , "pot" , "kettle" , "cup" , "mug" , "iphone" , "walking cane" , "spectacles" , "waterbottle", "brush" ,  "dustbin", "lamp", "coutch" , "television" , "car" , "mortorcycle" , "bed" , "towel" , "shampoo" , "toilet" , "door" , "chocolate" , "cleaning" , "scissors" , "laptop" , "computer" , "mobilephone" , "paper" , "books" , "computer mouse" , "charger" , "fan"]



#This list is used to search keywords. You can edit this list to search for google images of your choice. You can simply add and remove elements of the list.
#search_keyword = [ "blanket", "waterbottle", "brush" ,  "dustbin", "lamp", "coutch" , "television" , "car" , "mortorcycle" , "bed" , "towel" , "shampoo" , "toilet" , "door" , "chocolate" , "cleaning" , "scissors" , "laptop" , "computer" , "mobilephone" , "paper" , "books" , "computer mouse" , "charger" , "fan"]

#This list is used to further add suffix to your search term. Each element of the list will help you download 100 images. First element is blank which denotes that no suffix is added to the search keyword of the above list. You can edit the list by adding/deleting elements from it.So if the first element of the search_keyword is 'Australia' and the second element of keywords is 'high resolution', then it will search for 'Australia High Resolution'
keywords = ["" , "real" , "natural" ,"real+pictures" , "original" ,"flickr" ]


#Downloading entire Web Document (Raw Page Content)
def download_page(url):
    version = (3,0)
    cur_version = sys.version_info
    if cur_version >= version:     #If the Current Version of Python is 3.0 or above
        import urllib.request    #urllib library for Extracting web pages
        try:
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
            req = urllib.request.Request(url, headers = headers)
            resp = urllib.request.urlopen(req)
            respData = str(resp.read())
            return respData
        except Exception as e:
            print(str(e))
    else:                        #If the Current Version of Python is 2.x
        import urllib2
        try:
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
            req = urllib2.Request(url, headers = headers)
            response = urllib2.urlopen(req)
            page = response.read()
            return page
        except:
            return"Page Not found"


#Finding 'Next Image' from the given raw page
def _images_get_next_item(s):
    start_line = s.find('rg_di')
    if start_line == -1:    #If no links are found then give an error!
        end_quote = 0
        link = "no_links"
        return link, end_quote
    else:
        start_line = s.find('"class="rg_meta"')
        start_content = s.find('"ou"',start_line+1)
        end_content = s.find(',"ow"',start_content+1)
        content_raw = str(s[start_content+6:end_content-1])
        return content_raw, end_content


#Getting all links with the help of '_images_get_next_image'
def _images_get_all_items(page):
    items = []
    while True:
        item, end_content = _images_get_next_item(page)
        if item == "no_links":
            break
        else:
            items.append(item)      #Append all the links in the list named 'Links'
            #time.sleep(0.1)        #Timer could be used to slow down the request for image downloads
            page = page[end_content:]
    return items

# store images in 
# set the directory to store the items before call. Store in the current location
def _parallel_worker(items , keyword ,  start_index , end_index):
    idx = start_index;
    while(idx < end_index): 
        try:
            req = Request(items[idx], headers={"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})
            response = urlopen(req, timeout=100)
            output_file = open(str(keyword) +"_"+str(idx+1)+".img",'wb')
            data = response.read()
            output_file.write(data)
            response.close();

            print("completed ====> "+str(idx+1))
            idx = idx + 1;

        except IOError:   #If there is any IOError
            errorCount+=1
            print("IOError on image "+str(k+1))
            idx = idx + 1;
        except HTTPError as e:  #If there is any HTTPError
            errorCount+=1
            print("HTTPError"+str(k))
            idx = idx + 1;
        except URLError as e:
            errorCount+=1
            print("URLError "+str(k))
            idx = idx + 1;




############## Main Program ############
t0 = time.time()   #start the timer
#Download Image Links

DIR = "./images"

if not os.path.exists(DIR):
        os.mkdir(DIR)

i= 0
while i<len(search_keyword):
    items = []
    iteration = "Item no.: " + str(i+1) + " -->" + " Item name = " + str(search_keyword[i])
    print (iteration)
    print ("Evaluating...")
    search_keywords = search_keyword[i]
    search = search_keywords.replace(' ','%20')
    j = 0
    while j<len(keywords): # just one key word space
        pure_keyword = keywords[j].replace(' ','%20')
        url = "https://www.google.com/search?as_st=y&tbm=isch&hl=en&as_q="+ search + "+" +  pure_keyword + "&as_epq=&as_oq=&as_eq=&cr=&as_sitesearch=&safe=images&tbs=sur:fc"
        raw_html =  (download_page(url))
        items = items + (_images_get_all_items(raw_html))
        j = j + 1
    #print ("Image Links = "+str(items))
    print ("Total Image Links = "+str(len(items)))
    print ("\n")

    ## To save imges to the same directory
    # IN this saving process we are just skipping the URL if there is any error
    
    # Create a new directory for this kind of images and store within that directory

    if i != 0 : 
        os.chdir("../..") # move back to root where images dir is located

    DIR_TEMP = os.path.join(DIR , search_keyword[i])

    if not os.path.exists(DIR_TEMP):
        os.mkdir(DIR_TEMP)
    else:
        i = i+1
        os.chdir(DIR_TEMP) # Move to the existing dir, to take care of line 115
        continue

    # move to new directory to store images there
    os.chdir(DIR_TEMP)
 
    print ("Starting Download...")
    k=0
    errorCount=0

    # this is a good place to use different threads. 
    # divide the items between the number of threads avaliable
    num_threads =  multiprocessing.cpu_count()
    num_items_per_thread = len(items) / num_threads

    threads = []
    # Distribute work amoung threads
    for th in range(num_threads):
        thread = threading.Thread(target = _parallel_worker , args=(items , search_keyword[i] , th*num_items_per_thread , (th + 1)*num_items_per_thread, ) )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join() # Wait for all threads to complete before going to next search item


    print("\n")
    print("All are downloaded")
    print("\n"+str(errorCount)+" ----> total Errors")

    i = i+1
    items = []


t1 = time.time()    #stop the timer
total_time = t1-t0   #Calculating the total time required to crawl, find and download all the links of 60,000 images
print("Total time taken: "+str(total_time)+" Seconds")
#----End of the main program ----#
