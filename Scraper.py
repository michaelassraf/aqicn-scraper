from Scraper_Data import Scraper_Data
from Scraper_Meta import Scraper_Meta
import os,sys, global_values, time, datetime, uuid, zipfile, glob
from multiprocessing import Pool
from Scraper_Android import Scraper_Android
from time import sleep

#base_path = sys.argv[1]
#base_path = 'C:\\temp\\'

base_path = '/aerovibe-temp/AQICNScraper/'
base_execution_path = '/AQICNScraper/'
prxy_url = ''
#os.nice(15)

def getPercentage(unew, uold, start):
    return 100 * (float(unew) - float(uold)) / (time.time()-float(start))

test = Scraper_Meta(prxy_url + "http://aqicn.org/city/all/", 
                       {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'})
data = test.get_data()

def get_data(url):
    rand_name = ''
    folder_name = ''
    full_url = prxy_url + str(url)
    if global_values.debug:
        print str(datetime.datetime.now()) + " - Starting " + url
    try:
        test = Scraper_Data(full_url, {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'})
        with open(base_execution_path + "latest", "r") as myfile:
            folder_name = str(myfile.readline())
        rand_name = str(uuid.uuid4())
        data2 = test.get_data(base_path+folder_name+"//", rand_name)
        if data2 is not None:
            file_name = base_path+folder_name+"//"+rand_name+".txt"
            if global_values.debug:
                    print str(datetime.datetime.now()) + " - Prepare to save" + file_name
            with open(file_name, "a") as myfile:
                myfile.write(str(data2))
            if global_values.debug:
                print str(datetime.datetime.now()) + " - End " + url
    except Exception, e:
        file_name = base_path+folder_name+"//"+rand_name+".fail"
        with open(file_name, "a") as myfile:
            myfile.write(url)
        if global_values.debug:
            print str(datetime.datetime.now()) + " - Failed to collect data, the url is: " + url

def get_data_android(url):
    sleep(global_values.android_sleep)
    full_url = prxy_url + "http://mapidroid.aqicn.org/aqicn/json/android/" + str(url)
    if global_values.debug:
        print str(datetime.datetime.now()) + " - Starting " + full_url
    try:
        scraper  = Scraper_Android(full_url, {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'})
        folder_name = ''
        rand_name = str(uuid.uuid4())
        with open(base_execution_path + "latest_android", "r") as myfile:
            folder_name = str(myfile.readline())
        data2 = scraper.get_data(base_path+folder_name+"/", rand_name)
        if data2:
            file_name = base_path+folder_name+"/"+rand_name+".txt"
            with open(file_name, "a") as myfile:
                myfile.write(str(data2))
    except Exception, e:
        if global_values.debug:
            print str(datetime.datetime.now()) + " - Failed to collect data, the url is: " + full_url
            print str(datetime.datetime.now()) + " - Error is  - " + str(e)

def zip_folder(folder_path, output_path, type):
    file = ''
    if type == 1:
        file = zipfile.ZipFile(output_path+"//AQICNScraper.zip", "w")
    else:
        file = zipfile.ZipFile(output_path+"//AndroidScraper.zip", "w")
    for name in glob.glob(folder_path+"/*"):
        if ".txt" in name:
            file.write(name, os.path.basename(name), zipfile.ZIP_DEFLATED)
    file.close()

if __name__ == "__main__":
    #------------------------
    #
    # AQICN
    #
    #------------------------
    if global_values.debug:
        print str(datetime.datetime.now()) + " - Starting AQICN job !!!!!"
    timestamp = str(time.time())
    try:
        with open(base_execution_path + "latest", "r") as myfile:
            folder_name = str(myfile.readline())
            os.system("rm -rf /aerovibe-temp/AQICNScraper/"+folder_name)
    except:
        if global_values.debug:
            print str(datetime.datetime.now()) + " - No older crawls exist"
    with open(base_execution_path + "latest", "w+") as myfile:
        myfile.write(timestamp)
    if not os.path.exists(base_path +"//"+timestamp):
        os.makedirs(base_path +"//"+timestamp)
    p = Pool(global_values.num_threads)
    p.map(get_data, data)
    p.terminate()
    p.join()
    os.system("rm -rf /aerovibe-temp/AQICNScraper/" + timestamp + "/*.tmp")
    zip_folder("/aerovibe-temp/AQICNScraper/" + timestamp, "/aerovibe-temp/latestTar", 1)
    if global_values.debug:
        print str(datetime.datetime.now()) + " - Ending AQICN job !!!!!!!"
    #------------------------
    #
    # Android
    #
    #------------------------
    if global_values.debug:
        print str(datetime.datetime.now()) + " - Starting Android job !!!!!"
    timestamp_android = str(time.time())
    try:
        with open(base_execution_path + "latest_android", "r") as myfile:
            folder_name = str(myfile.readline())
            os.system("rm -rf /aerovibe-temp/AQICNScraper/"+folder_name)
    except:
        if global_values.debug:
            print str(datetime.datetime.now()) + " - No older crawls exist"
    with open(base_execution_path + "latest_android", "w+") as myfile:
        myfile.write(timestamp_android)
    if not os.path.exists(base_path +"//"+timestamp_android):
        os.makedirs(base_path +"//"+timestamp_android)
    data_android = ''
    with open("/AQICNScraper/android_values.txt", "r") as myfile:
        data_android = myfile.readlines()
    p = Pool(global_values.android_threads)
    p.map(get_data_android, data_android)
    p.terminate()
    p.join()
    os.system("rm -rf /aerovibe-temp/AQICNScraper/" + timestamp_android + "/*.tmp")
    zip_folder("/aerovibe-temp/AQICNScraper/" + timestamp_android, "/aerovibe-temp/latestTar", 2)
    if global_values.debug:
        print str(datetime.datetime.now()) + " - Ending Android job !!!!!!!"
        print str(datetime.datetime.now()) + " - Ending Execution !!!!!!!"
    os.system("rm -f /tmp/AQICNScrpaer.log")
    os.system("/bin/python2.7 /AQICNScraper/Scraper.py >> /tmp/AQICNScrpaer.log 2>&1 &")
    
    sys.exit()
    
