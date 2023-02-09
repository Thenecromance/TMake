# coding=utf-8
import os
import sys
import platform
import subprocess
import shutil


Python = "python" if platform.system() == "Windows" else "python3"


def executCommand(command):
    out = open(os.devnull, 'w')
    err = subprocess.STDOUT
    return subprocess.call(command, shell=True, stdout=out, stderr=err)


def runScript(Script, Params):
    if os.system(Python + " " + Script + " " + Params) != 0:
        print("Unable to run " + Script)
        exit(255)


def CopySelf(targetPath):
    if not os.path.exists(targetPath):
        shutil.copy()
        pass


# python recheck
if executCommand(Python + " --version") != 0:
    print("Make sure Python can be started from the command line (add path to `python.exe` to PATH on Windows)")
    exit(255)
# cmake check
if executCommand("cmake --version") != 0:
    print("No CMake")
    exit(255)
# git check
if executCommand("git --version") != 0:
    print("No Gits")
    exit(255)
    
cwd = os.getcwd()
runScript( os.path.join(cwd,"TMake","python", "bootstrap.py"), cwd)
print("\nMonkey Initialize complete!\n")
