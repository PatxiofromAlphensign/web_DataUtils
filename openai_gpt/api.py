import requests
import xml.etree.ElementTree as ET
from download_model import Downloader

class reqobject_search:
    def __init__(self, q=None):
        self.req = requests.get("https://storage.googleapis.com/gpt-2/")
        req = self.req
        self.all_posible_reqobject = {}
        for attr in dir(req):
            self.all_posible_reqobject[attr] =  getattr(req, attr)
    def __getitem__(self, k : int):
        dict_key = [ key for key in self.all_posible_reqobject.keys() if '__' not in key][k]
        return self.all_posible_reqobject[dict_key]
    
    def __iter__(self):
        return self.all_posible_reqobject.values()
if __name__ == '__main__':
    Downloader('2M').download()

    # print(reqobject_search().req.text)
