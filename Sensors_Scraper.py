from bs4 import BeautifulSoup
import urllib2,re,global_values

class Sensors_Scraper:
    def __init__(self, url, user_agent, proxy_ip = None, proxy_port = None):
        self.url = url
        self.user_agent = user_agent
        self.proxy_ip = proxy_ip
        self.proxy_port = proxy_port
        if proxy_ip is not None:
            print 'todo'
        else:
            self.req = urllib2.Request(self.url, headers=self.user_agent)
        '''
        try:
            self.raw_data = urllib2.urlopen(self.req)
        except urllib2.HTTPError, error:
            contents = error.read()
            if global_values.debug:
                print contents'''
            
    def get_data(self):
        try:
            data_dict = {}
            
            #------------------------
            #
            # Data extraction
            #
            #------------------------
        
            soup = BeautifulSoup(urllib2.urlopen(self.req).read())
            i = 0
            for a in soup.find_all('a', href=True):
                state = re.search('/city/(.*?)/', a['href'])
                if state:
                    if not data_dict.has_key(state.group(1)):
                        data_dict[state.group(1)] = list()
                    data_dict[state.group(1)].append(a['href'])
            return data_dict
        except urllib2.HTTPError, e:
            if global_values.debug:
                print e.fp.read()
    
    
