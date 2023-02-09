# coding=utf-8

# this script is mainly trying to instead the CMake or .gitmodule or something else
# and according to my idea,prepare to let this script support ssl , .git , resources etc

import getopt
import platform
import shutil
import subprocess
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
            super().__init__('bootstrap.log', level=logging.DEBUG)
            # self =logging.getLogger('bootstrap.log')
            # self.setLevel(logging.DEBUG)
            file_handler = logging.FileHandler('bootstrap.log')
            formatter = logging.Formatter(
                '[Monkey][%(asctime)s][%(levelname)s]:%(message)s')
            stream_handler = logging.StreamHandler(sys.stdout)
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


# try:
#     from progressbar import *
#     import time
#     total =1000

#     def do():
#         time.sleep(0.01)
#     progressbar = Progressbar()
#     for i in progressbar(range(1000)):
#         do()

# except:
#     logger.warning("current OS does not install the prograssbar")


# FUCKING DNS cache pollution by some **** reason in ****** and
# protect me in some pc don't have V*N and speed up for some project
USE_MIRROR: bool = True
MIRROR_WRB_LIST = {
    'https://github.com/': 'https://kgithub.com/',
    #    'gitlab.com':''
}

# FILE_EXT ="bot"

SRC_DIR_BASE = "src"
SRC_DIR = "src"
DEBUG_OUTPUT = False

TOOL_COMMAND_GIT = "git"
TOOL_COMMAND_SVN = "svn"

def dieIfNonZero(res):
    if res != 0:
        raise ValueError("Command returned non-zero status: " + str(res))
    
def executeCommand(command, printCommand=False, quiet=False):

    printCommand = printCommand or DEBUG_OUTPUT
    out = None
    err = None

    if quiet:
        out = open(os.devnull, 'w')
        err = subprocess.STDOUT

    if printCommand:
        logger.debug(">>> " + command)

    return subprocess.call(command, shell=True, stdout=out, stderr=err)

class BootstrapRoot:
    def __init__(self, parent_dir_path):
        self.parent_dir_path = parent_dir_path
        self.file_name = os.path.join(self.parent_dir_path,'bootstrap_path.json')
    def load(self):
        with open(self.file_name) as f:
            paths_data = json.load(f)
        for path_data in paths_data:
            if not path_data["ignore"]:
                obj = BootstrapLoader(self.parent_dir_path + "/" + path_data["path"])
                obj.Download()
                if(obj.load_status == False):
                    logger.error("fail to download :"+ obj.GetFilePath())
                
class BootstrapLoader:
    
    default_dir = None 
    default_file_name = 'bootstrap.json'
    default_mark_file = '.'+default_file_name
    load_status = False
    
    def __init__(self, dir) -> None:
        self.default_dir = dir
        pass
    
    def GetLoadStatus(self):
        return self.load_status
    
    def GetFilePath(self):
        return os.path.join(self.default_dir , self.default_file_name)
    
    def GetMarkPath(self):
        return os.path.join(self.default_dir,self.default_mark_file)
    
    def ComputeHash(self,path ):
        if(self.FileExist(path) is False):
            return "-1"
        blocksize = 65536
        hasher = hashlib.sha1()
        with open(path, 'rb') as afile:
            buf = afile.read(blocksize)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(blocksize)
        return hasher.hexdigest()
         
    def FileExist(self, path ):
        return os.path.exists(path)
    
    def MarkAsRead(self):
        if(self.FileExist(self.GetMarkPath())):
            os.remove(self.GetMarkPath())
        logger.info("Mark "+self.GetFilePath()+"  as read" )
        shutil.copy2(self.GetFilePath(),self.GetMarkPath())
    
    def ReadJSONData(self):
        try:
            json_data = open(self.GetFilePath()).read()
        except:
            logger.exception("Fail to load Json file:" + self.GetFilePath())
            exit(255)
        try:
            with open(self.GetFilePath()) as f :
                data = json.load(f)
        except:
            logger.info(self.GetFilePath())
            logger.exception("Fail to parse Json data")
            exit(255)
        return data
        
    def useMirrorReplace(self ,url: string) -> any:
        if MIRROR_WRB_LIST is None or MIRROR_WRB_LIST == {}:
            logger.error(
                "You are setting USE_MIRROR as True but not set MIRROR_WRB_LIST, nothing will happend")
            USE_MIRROR = False
            return url
        for origin_url, mirror_url in MIRROR_WRB_LIST.items():
            if url.find(origin_url) != -1:
                url = url.replace(origin_url, mirror_url)
                break
        logger.info(url)
        return url
    def escapifyPath(self, path):
        if path.find(" ") == -1:
            return path
        if platform.system() == "Windows":
            return "\"" + path + "\""
        return path.replace("\\ ", " ")
    
    def downloadFile(self , url, download_dir, sha1_hash=None, force_download=False, user_agent=None):
        # if not os.path.isdir(download_dir):
        #     os.mkdir(download_dir)

        if USE_MIRROR:
            url = self.useMirrorReplace(url)

        p = urlparse(url)
        # replace special characters in the URL path
        url = urlunparse([p[0], p[1], quote(p[2]), p[3], p[4], p[5]])
        filename_rel = os.path.split(p.path)[1]
        target_filename = os.path.join(download_dir, filename_rel)
        if force_download is False and os.path.exists(target_filename) and sha1_hash is not None and sha1_hash != "":
            hash_file = self.ComputeHash(target_filename)
            if hash_file != sha1_hash:
                logger.info("Hash of " + target_filename + " (" + hash_file +
                            ") does not match expected hash (" + sha1_hash + "); forcing download")
                force_download = True

        # download
        if (not os.path.exists(target_filename)) or force_download:
            logger.info("Downloading " + url + " to " + target_filename)
            if p.scheme == "ssh":
                logger.error("so far could not support ssl")
            else:
                if user_agent is not None:
                    opener = urllib.request.build_opener()
                    opener.addheaders = [('User-agent', user_agent)]
                    f = open(target_filename, 'wb')
                    f.write(opener.open(url).read())
                    f.close()
                else:
                    urlretrieve(url, target_filename)
        else:
            logger.info("Skipping download file " + url + " already exists")
        # check SHA1 hash
        if sha1_hash is not None and sha1_hash != "":
            hash_file = computeFileHash(target_filename)
            if hash_file != sha1_hash:
                raise RuntimeError("Hash of " + target_filename + " (" +
                                   hash_file + ") differs from expected hash (" + sha1_hash + ")")

        return target_filename

    def cloneRepository(self , type, url, target_name, revision=None, try_only_local_operations=False):

        if USE_MIRROR:
            url = self.useMirrorReplace(url)

        target_dir = self.escapifyPath(target_name)
        target_dir_exists = os.path.exists(target_dir)
        logger.info("Cloning " + url + " to " + target_dir)

        if type == "git":
            repo_exists = os.path.exists(os.path.join(target_dir, ".git"))

            if not repo_exists:
                if try_only_local_operations:
                    raise RuntimeError("Repository for " + target_name +
                                       " not found; cannot execute local operations only")
                if target_dir_exists:
                    logger.info("Removing directory " +
                                target_dir + " before cloning")
                    shutil.rmtree(target_dir)
                dieIfNonZero(executeCommand(TOOL_COMMAND_GIT +
                             " clone --recursive " + url + " " + target_dir))
            elif not try_only_local_operations:
                logger.info("Repository " + target_dir +
                            " already exists; fetching instead of cloning")
                dieIfNonZero(executeCommand(TOOL_COMMAND_GIT + " -C " +
                             target_dir + " fetch --recurse-submodules"))

            if revision is None:
                revision = "HEAD"
            dieIfNonZero(executeCommand(TOOL_COMMAND_GIT + " -C " +
                         target_dir + " reset --hard " + revision))
            dieIfNonZero(executeCommand(TOOL_COMMAND_GIT +
                         " -C " + target_dir + " clean -fxd"))

        elif type == "svn":
            if not try_only_local_operations:  # we can't do much without a server connection when dealing with SVN
                if target_dir_exists:
                    logger.info("Removing directory " +
                                target_dir + " before cloning")
                    shutil.rmtree(target_dir)
                dieIfNonZero(executeCommand(TOOL_COMMAND_SVN +
                             " checkout " + url + " " + target_dir))

            if revision is not None and revision != "":
                raise RuntimeError("Updating to revision not implemented for SVN.")

        else:
            raise ValueError("Cloning " + type + " repositories not implemented.")
        logger.info("")

    def Download(self):
        if(self.ComputeHash(self.GetFilePath()) == self.ComputeHash(self.GetMarkPath())):
            logger.info("ignored file:"+ self.GetFilePath())
            self.load_status = True
            return
        
        if(self.FileExist(self.GetFilePath())==False):
            logger.error("file does not exist")
            exit(255)
            
        data =  self.ReadJSONData()
        if data is None:
            logger.error("Load json file failed! "+self.GetFilePath())
            exit(255)
            
        for obj in data:
            if obj["source"]["type"] == "git" or obj["source"]["type"] == "svn":
                self.cloneRepository(
                    obj["source"]["type"], obj["source"]["url"],
                    os.path.join(self.default_dir, obj["name"])
                    )
            else:
                self.downloadFile(obj["source"]["url"],
                    self.default_dir
                    )
        
        self.MarkAsRead()
        

if __name__ == "__main__":
    root = BootstrapRoot(sys.argv[1])
    root.load()
