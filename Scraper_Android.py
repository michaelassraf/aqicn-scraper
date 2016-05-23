import global_values,json,datetime,urllib

class Scraper_Android:
    def __init__(self, url, user_agent, proxy_ip = None, proxy_port = None):
        self.url = url
        self.user_agent = user_agent
        self.proxy_ip = proxy_ip
        self.proxy_port = proxy_port
        self.counter = 1
    
    def get_first_element(self, data):
        try:
            data_type = type(data)
            if data_type is list:
                return str(data.pop(0))
            elif data_type is dict:
                return str(data.itervalues().next())
        except:
            return False
        return False
    
    def get_data(self, path, fname):
        status = 0
        full_file_path = str(path) + str(fname) + ".tmp"
        if global_values.debug:
           print str(datetime.datetime.now()) + " - Starting to download JSON - " + full_file_path
        while status == 0:
            self.counter += 1
            if self.counter == global_values.url_retry:
                status = 2
            try:
                urllib.urlretrieve(self.url, full_file_path)
                status = 1 
            except:
                if global_values.debug:
                    print str(datetime.datetime.now()) + " - Failed to download JSON - " + self.url
        
        if status == 1:
            try:
                with open(full_file_path, "r") as myfile:
                    if global_values.debug:
                        print str(datetime.datetime.now()) + " - Start parsing - " + full_file_path
                    data_dict = {}
                    json_obj = json.loads(myfile.read())
         
                    if json_obj.has_key('historic') and json_obj['historic'].has_key('PM2.5'):   
                        pm25arr = self.get_first_element(json_obj['historic']['PM2.5'])
                        if pm25arr:
                            data_dict['PM2_5'] = pm25arr
                    
                    if json_obj.has_key('historic') and json_obj['historic'].has_key('PM10'):    
                        pm10arr = self.get_first_element(json_obj['historic']['PM10'])
                        if pm10arr:
                            data_dict['PM10'] = pm10arr
                    
                    if json_obj.has_key('historic') and json_obj['historic'].has_key('O3'):      
                        o3arr = self.get_first_element(json_obj['historic']['O3'])
                        if o3arr:
                            data_dict['O3'] = o3arr
                    
                    if json_obj.has_key('historic') and json_obj['historic'].has_key('no2'):
                        no2arr = self.get_first_element(json_obj['historic']['no2'])
                        if no2arr:
                            data_dict['No2'] = no2arr
                    
                    if json_obj.has_key('historic') and json_obj['historic'].has_key('so2'):    
                        so2arr = self.get_first_element(json_obj['historic']['so2'])
                        if so2arr:
                            data_dict['So2'] = so2arr
                    
                    if json_obj.has_key('historic') and json_obj['historic'].has_key('t'):    
                        temp = self.get_first_element(json_obj['historic']['t'])
                        if temp:
                            data_dict['Temperature'] = temp
                    
                    if json_obj.has_key('historic') and json_obj['historic'].has_key('co'):    
                        coarr = self.get_first_element(json_obj['historic']['co'])
                        if coarr:
                            data_dict['Humidity'] = coarr
                    
                    if json_obj.has_key('historic') and json_obj['historic'].has_key('h'):
                        humidity = self.get_first_element(json_obj['historic']['h'])
                        if humidity:
                            data_dict['Humidity'] = humidity
                    
                    if json_obj.has_key('historic') and json_obj['historic'].has_key('w'):
                        wind = self.get_first_element(json_obj['historic']['w'])
                        if wind:
                            data_dict['Wind'] = wind
                    
                    data_dict['Name'] = str(json_obj['nameen'])
                    data_dict['URL'] = self.url
                    if json_obj['time']:
                        data_dict['Timestamp'] = str(json_obj['time'])
                    else:
                        data_dict['Timestamp'] = str(json_obj['nearest'][0]['t'])
                    data_dict['Coordinates'] = str(json_obj['nearest'][0]['g'][0])+ "," + str(json_obj['nearest'][0]['g'][1])
                    
                    if global_values.debug:
                        print str(datetime.datetime.now()) + " - Done parsing - " + full_file_path
                    
                    return json.dumps(data_dict, ensure_ascii=False)
            except Exception, e:
                if global_values.debug:
                    print str(datetime.datetime.now()) + " - Failed to parse JSON - " + self.url
                    print str(datetime.datetime.now()) + " - Error is  - " + str(e)
                return False
            
            
        
        
        
        