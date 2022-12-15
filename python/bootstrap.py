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

SRC_DIR_BASE = "src"
SRC_DIR = "src"
DEBUG_OUTPUT = False

TOOL_COMMAND_GIT = "git"
TOOL_COMMAND_SVN = "svn"


def computeFileHash(filename):
    blocksize = 65536
    hasher = hashlib.sha1()
    with open(filename, 'rb') as afile:
        buf = afile.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(blocksize)
    return hasher.hexdigest()


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


def escapifyPath(path):
    if path.find(" ") == -1:
        return path
    if platform.system() == "Windows":
        return "\"" + path + "\""
    return path.replace("\\ ", " ")


def useMirrorReplace(url: string) -> any:
    if MIRROR_WRB_LIST is None or MIRROR_WRB_LIST == {}:
        logger.error(
            "You are setting USE_MIRROR as True but not set MIRROR_WRB_LIST, nothing will happend")
        USE_MIRROR = False
        return url
    for origin_url, mirror_url in  MIRROR_WRB_LIST.items():
        if url.find(origin_url) is not -1:
            url = url.replace(origin_url, mirror_url)
            break
    logger.info(url)
    return url


def downloadFile(url, download_dir, sha1_hash=None, force_download=False, user_agent=None):
    if not os.path.isdir(download_dir):
        os.mkdir(download_dir)
        
    if USE_MIRROR:
        url = useMirrorReplace(url)

    p = urlparse(url)
    # replace special characters in the URL path
    url = urlunparse([p[0], p[1], quote(p[2]), p[3], p[4], p[5]])
    filename_rel = os.path.split(p.path)[1]
    target_filename = os.path.join(download_dir, filename_rel)
    if force_download is False and os.path.exists(target_filename) and sha1_hash is not None and sha1_hash != "":
        hash_file = computeFileHash(target_filename)
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


def cloneRepository(type, url, target_name, revision=None, try_only_local_operations=False):
    
    if USE_MIRROR:
        url = useMirrorReplace(url)  
    
    target_dir = escapifyPath(target_name)
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


def readSubRootData(ignoreDir=True):
    """
    get which subroots' resrouces will be downloaded 
    file example: 
    [
        {
            "ignore":false,
            "path":"directory path, in this directory must contain the bootstrap.json"
        },
        {
            "ignor":true,
            "path":""
        }
    ]
    """
    file_name = os.path.join("bootstrap_path.json")
    data = readJSONData(file_name)
    if data is None:
        logger.error("Could not find the " + file_name + " in the root path")
        exit(255)
    sub_path_list = []
    if ignoreDir is False:
        logger.warning("All the file will be download")

    for sub_data in data:
        if os.path.isdir(sub_data.get("path")) is not True:
            createSubDirectory(sub_data.get("path"))
            exit(255)
        else:
            if ignoreDir == True:
                if sub_data.get("ignore") is False:
                    sub_path_list.append(sub_data.get("path"))
            else:
                sub_path_list.append(sub_data.get("path"))

    if len(sub_path_list) == 0:
        return exit(255)
    
    markFileAsRead(file_name)
    return sub_path_list


def readResourceInDir(dir_path):
    """
    read an download the bootstrap.json
    [
        {
            "name":"file name",
            "source":{
                "type": "git",
                "url":"gits",
                "revision": "0.9.9.8",
                "user_agent":""
            }
        }
    ]
    """
    config_file = os.path.join(dir_path, "bootstrap.json")
    # check file exist or not
    if not os.path.exists(config_file):
        logger.error("could not find " + config_file + " in " + dir_path + "!")
        exit(255)
    # load data from the json
    data = readJSONData(config_file)
    if data is None:
        logger.error("Invaild json file :" + config_file)
        exit(255)
    for obj in data:
        cloneRepository(
            obj["source"]["type"], obj["source"]["url"],
            os.path.join(dir_path, obj["name"])
        )
    markFileAsRead(config_file)


def createSubDirectory(dir_path):
    os.mkdir(dir_path)

    bootstrap_file = os.path.join(dir_path, "demo.json")
    logger.error(
        dir_path + " is not a invaild path more detail please to see : " + bootstrap_file)
    data = [
        {
            "name": "file name",
            "source": {
                "type": "git",
                "url": "gits",
                "revision": "0.9.9.8",
                "user_agent": ""
            }
        }
    ]
    writeJSONData(data, bootstrap_file)


def readJSONData(filename):
    try:
        json_data = open(filename).read()
    except:
        logger.exception("Fail to load Json file:" + filename)
        exit(255)
    try:
        data = json.loads(json_data)
    except:
        logger.exception("Fail to parse Json data")
        exit(255)
    return data


def writeJSONData(data, filename):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)


def printOptions():
    print("I'm tooooooo lazy")


def cleanupLogFile():
    if os .path.exists("bootstrap.log"):
        with open('bootstrap.log', 'w') as f:
            f.write("")
            f.close()

def markFileAsRead(file_name):
    shutil.copy(file_name,"."+file_name)

def main(argv):
    try:
        opts, args = getopt.getopt(
            argv,
            "f"
        )
    except getopt.GetoptError:
        printOptions()
        return 0

    cleanupLogFile()
    logger.info("Monkey is trying to use Python logging~")
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            printOptions()
            return 0
        if opt in ("-f"):
            lists = readSubRootData(arg)
            if lists is not None:
                for subdir in lists:
                    readResourceInDir(subdir)
            else:
                exit(255)
    
    
    


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
