from bs4 import BeautifulSoup
import urllib2,re,global_values

class Scraper_Meta:
    def __init__(self, url, user_agent, proxy_ip = None, proxy_port = None):
        self.url = url
        self.user_agent = user_agent
        self.proxy_ip = proxy_ip
        self.proxy_port = proxy_port
        if proxy_ip is not None:
            print 'todo'
        else:
            self.req = urllib2.Request(self.url, headers=self.user_agent)
            
    def get_data(self):
        try:
            sensors_list = list()
            
            #------------------------
            #
            # Data extraction
            #
            #------------------------
            soup = BeautifulSoup(urllib2.urlopen(self.req).read())
            for a in soup.find_all('a', href=True):
                state = re.search('/city/(.*?)/', a['href'])
                if state:
                    sensors_list.append(a['href'])
            return sensors_list
        except urllib2.HTTPError, e:
            if global_values.debug:
                print "Failed to collect sensors"