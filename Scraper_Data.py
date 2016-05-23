import urllib2,string,global_values,re,json
from bs4 import BeautifulSoup
import datetime
import os
import random
from time import sleep

class Scraper_Data:
    def __init__(self, url, user_agent, proxy_ip = None, proxy_port = None):
        self.url = url
        self.user_agent = user_agent
        self.proxy_ip = proxy_ip
        self.proxy_port = proxy_port
        self.counter = 1
            
    def get_data(self, path, fname):
        status = 0
        full_file_path = path + fname + ".tmp"
        while status == 0:
            if self.counter == global_values.url_retry:
                status = 2
            try:
                if self.counter % 2 == 0:
                    proxy_url = ""
                    wget_command = "wget --user-agent=" + global_values.user_agent + " " + proxy_url + self.url + " -O " + full_file_path
                    os.system(wget_command + " > /dev/null 2>&1")
                    if global_values.debug:
                        print str(datetime.datetime.now()) + " - Download via Proxy - " + proxy_url + self.url
                else:
                    wget_command = "wget --user-agent=" + global_values.user_agent + " " + self.url + " -O " + full_file_path
                    os.system(wget_command + " > /dev/null 2>&1")
                    if global_values.debug:
                        print str(datetime.datetime.now()) + " - Download via Wget - " + self.url
            except:
                if global_values.debug:
                    print str(datetime.datetime.now()) + " - Download failed - " + self.url
            if os.path.isfile(full_file_path):
                if os.path.getsize(full_file_path) > 0:
                    status = 1
                else:
                    self.counter += 1
                    if global_values.debug:
                        print str(datetime.datetime.now()) + " - Download failed, going to sleep - " + self.url
                    sleep(random.randint(1,100))
        
        if os.path.isfile(full_file_path):
            if os.path.getsize(full_file_path) == 0:
                os.system("rm -f " + full_file_path)
        if status == 1:
            try:
                data_dict = {}            
                
                #------------------------
                #
                # Data extraction
                #
                #------------------------
                
                file_read = open(full_file_path, 'r')
                soup_temp = BeautifulSoup(file_read.read())
                temp_data = soup_temp.find("div", {"id": "citydivmain"})
                soup = BeautifulSoup(str(temp_data))
         
                pm25arr = soup.find_all(id="cur_pm25")
                if pm25arr:
                    data_dict['PM2_5'] = pm25arr[0].text
                    
                pm10arr = soup.find_all(id="cur_pm10")
                if pm10arr:
                    data_dict['PM10'] = pm10arr[0].text
                    
                o3arr = soup.find_all(id="cur_o3")
                if o3arr:
                    data_dict['O3'] = o3arr[0].text
                
                no2arr = soup.find_all(id="cur_no2")
                if no2arr:
                    data_dict['No2'] = no2arr[0].text
                    
                so2arr = soup.find_all(id="cur_so2")
                if so2arr:
                    data_dict['So2'] = so2arr[0].text
                    
                temp = soup.find_all(id="cur_t")
                if temp:
                    data_dict['Temperature'] = temp[0].text
                    
                pressure = soup.find_all(id="cur_p")
                if pressure:
                    data_dict['Pressure'] = pressure[0].text
                
                humidity = soup.find_all(id="cur_h")
                if humidity:
                    data_dict['Humidity'] = humidity[0].text
                
                wind = soup.find_all(id="cur_w")
                if wind:
                    data_dict['Wind'] = wind[0].text
                
                name = re.match('(.*)\Real-time', soup.find(id="aqiwgttitle2").text).group(1) # Get the sensor name
                name = name[1:]
                name = name [:-1]
                data_dict['Name'] = name
                data_dict['URL'] = self.url
            
                #---------------------------------
                #
                # Coordinates and time extraction
                #
                #--------------------------------
            
                script = soup_temp.find('script', text=re.compile('mapStationData'))
                text = script.text
                temp_text = ''
                try:
                    temp_text = re.search('\{(.*?)'+name+'(.*?)\}', text)
                except:
                    temp_text = re.search('\{(.*?)'+json.dumps(u''.join(name))+'(.*?)\}', text)
                temp_text_time2 = string.split(temp_text.group(1), "aqi")
                coordinates = re.search('\"g\"\:\[(.*?)\]', temp_text.group(2))
                time = re.search('\"utime\"\:\" on (.*?)\",', temp_text_time2[-1])
                data_dict['Coordinates'] = coordinates.group(1)
                data_dict['Time'] = time.group(1)
                if global_values.debug:
                    print str(datetime.datetime.now()) + " - Parsing Successful" + full_file_path
                return json.dumps(data_dict, ensure_ascii=False)
            except urllib2.HTTPError, e:
                if global_values.debug:
                    print str(datetime.datetime.now()) + " - Failed to parse data " + self.url
                return False
        else:
            return False
