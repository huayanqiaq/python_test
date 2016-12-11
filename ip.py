# -*- coding:utf-8 -*-

import sys
import urllib2
import json

def get_ip_information(ip):
    url='http://api.map.baidu.com/highacciploc/v1?qcip='+ip+'&qterm=pc&ak=uHX5ddNcCBPKMyquTKE6qdyHukHEC4u7&coord=bd09ll&extensions=3'
    poiss=''
    request = urllib2.Request(url)
    page = urllib2.urlopen(request, timeout=10)
    data_json = page.read()
    data_dic = json.loads(data_json)
    if(data_dic.has_key("content")):
        content=data_dic["content"]
        address_component=content["address_component"]
        formatted_address=content["formatted_address"]
        print "gai ip juti weizhi wei:"
        print address_component["country"]
        print formatted_address
        if (content.has_key("pois")):
            print "gai ip de POI xinxi ruxia:"
            pois = content["pois"]
            for index in range(len(pois)):
                pois_name = pois[index]["name"]
                pois_address = pois[index]["address"]
                print pois_name, pois_address
    else:
        print 'ip dizhi dingwei shibai'
if __name__ == '__main__':
    get_ip_information(sys.argv[1])
    #print sys.argv[1]