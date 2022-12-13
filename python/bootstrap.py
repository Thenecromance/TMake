#utf-8 

#this script is mainly trying to instead the CMake or .gitmodule or something else 
#and according to my idea,prepare to let this script support ssl , .git , resources etc

import sys
import json
import hashlib
import urllib
import ssl
import os
import re
import string


try:
    from urllib.request import urlparse
    from urllib.request import urlunparse
    from urllib.request import urlretrieve
    from urllib.request import quote
except ImportError:
    from urlparse import urlparse
    from urlparse import urlunparse
    from urllib import urlretrieve
    from urllib import URLopener
    from urllib import quote
    
try:
    import logging
    class TLog(logging.Logger):        
        def __init__(self) -> None:
                super().__init__('bootstrap.log',level=logging.DEBUG)
                # self =logging.getLogger('bootstrap.log')
                # self.setLevel(logging.DEBUG)
                file_handler = logging.FileHandler('bootstrap.log')
                formatter = logging.Formatter('[%(asctime)s][%(levelname)s]:%(message)s')
                stream_handler =logging.StreamHandler(sys.stdout)
                file_handler.setFormatter(formatter)
                stream_handler.setFormatter(formatter)
                self.addHandler(file_handler)
                self.addHandler(stream_handler)
except ImportError:
    class TLog:
        def __init__(self) -> None:
            pass
        def debug(self, msg):
            print(msg)
        def info(self, msg):
            print(msg)
        def warning(self, msg):
            print(msg)
        def error(self, msg):
            print(msg)
        def exception(self, msg):
            print(msg)
        def fatal(self, msg):
            print(msg)  
logger = TLog()

#FUCKING DNS cache pollution by some **** reason in ****** and
#protect me in some pc don't have V*N and speed up for some project 
USE_MIRROR:bool = False
MIRROR_WRB_LIST ={ 
                #    'github.com':'',
                #    'gitlab.com':''
                  }

SRC_DIR_BASE = "src"


def computeFileHash(filename):
    blocksize = 65536
    hasher = hashlib.sha1()
    with open(filename,'rb') as afile:
        buf = afile.read(blocksize)
        while len(buf)>0:
            hasher.update(buf)
            buf = afile.read(blocksize)
    return hasher.hexdigest()

def useMirrorReplace( url:string) ->any:
    if MIRROR_WRB_LIST is None or MIRROR_WRB_LIST == {}:
        logger.error("You are setting USE_MIRROR as True but not set MIRROR_WRB_LIST, nothing will happend")
        USE_MIRROR= False
        return url 
    for origin_url,mirror_url in MIRROR_WRB_LIST:
        if url.find(origin_url) is not -1 :
            url = url.replace(origin_url, mirror_url)
            break
    return url 


def downloadFile(url, download_dir , sha1_hash = None , force_download = False , user_agent = None ):
    if not os.path.isdir(download_dir):
        os.mkdir(download_dir)
    
    if USE_MIRROR:
        url  = useMirrorReplace(url)
    
    
    p = urlparse(url)
    url = urlunparse([p[0], p[1], quote(p[2]), p[3], p[4], p[5]]) # replace special characters in the URL path
    filename_rel = os.path.split(p.path)[1]
    target_filename = os.path.join(download_dir,filename_rel)
    if force_download is False and os.path.exists(target_filename) and sha1_hash is not None and sha1_hash !="":
        hash_file = computeFileHash(target_filename)
        if hash_file!= sha1_hash:
            logger.info("Hash of " + target_filename + " ("+ hash_file + ") does not match expected hash (" + sha1_hash + "); forcing download")
            force_download = True
    
    #download 
    if (not os.path.exists(target_filename)) or force_download:
        logger.info("Downloading " + url + " to " + target_filename)
        if p.scheme == "ssh":
            logger.error("so far could not support ssl")
        else :
            if user_agent is not None:
                opener = urllib.request.build_opener()
                opener.addheaders = [('User-agent',user_agent)]
                f = open(target_filename , 'wb')
                f.write(opener.open(url).read())
                f.close()
            else:
                urlretrieve(url,target_filename)                 
    else:
        logger.info("Skipping download file "+ url + " already exists")
    # check SHA1 hash
    if sha1_hash is not None and sha1_hash != "":
        hash_file = computeFileHash(target_filename)
        if hash_file != sha1_hash:
            raise RuntimeError("Hash of " + target_filename + " (" + hash_file + ") differs from expected hash (" + sha1_hash + ")")

    return target_filename

def readSubRootData(file_name , ignoreFile  =True):
    """
    get which subroots' resrouces will be downloaded 
    """
    data =  readJSONData(file_name)
    if data is None: 
        logger.error("Could not find the " + file_name + " in the root path")
        return None 
    sub_path_list = []
    if ignoreFile is False:
        logger.info("All the file will be download")
        
    for sub_data in data :
        if (ignoreFile and sub_data["ignore"] is True) is not True:
            logger.info("Get dir path" + sub_data["path"])
            if os.path.isdir(sub_data["path"]) is not True:
                logger.error(sub_data["path"] +"is not a invaild path")
            else:
                sub_path_list.append(sub_data["path"])
            
    if len(sub_path_list) is 0 :
        return None 
    return sub_path_list
    
def readJSONData(filename):
    try:
        json_data = open(filename).read()
    except:
        logger.exception("Fail to load Json file:" +filename)
        return None 
    try:
        data = json.load(json_data)
    except:
        logger.exception("Fail to parse Json data")
        return None 
    return data

def writeJSONData(data, filename):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)


def main(argv):
    logger.info("TLog Test")
    pass


if __name__ =="__main__":
    sys.exit(main(sys.argv[1:]))
    