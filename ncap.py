import json
import zipfile
import os
import sys
import colorama
import datetime
from colorama import Fore, Back, Style
ncapversion="v0.0.1"
def jifwrite(jarf, imagefp, icontent):
    temp = "temp_jar_extraction"
    os.makedirs(temp, exist_ok=True)

    try:
        tempfp = os.path.join(temp, os.path.basename(imagefp))
        with open(tempfp, 'wb') as f:
            f.write(icontent)
        with zipfile.ZipFile(jarf, 'a') as jar:
            jar.write(tempfp, arcname=imagefp)

    finally:
        if os.path.exists(temp):
            for root, dirs, files in os.walk(temp, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(temp)

def jfexists(jarf, ftcheck):
    with zipfile.ZipFile(jarf, 'r') as jar:
        flist = jar.namelist()
        return ftcheck in flist

def jfread(jarf, read):
    temp = "temp_jar_extraction"
    os.makedirs(temp, exist_ok=True)

    try:
        with zipfile.ZipFile(jarf, 'r') as jar:
            jar.extract(read, path=temp)

        extractedfp = os.path.join(temp, read)
        with open(extractedfp, 'r') as f:
            fcontent = f.read()

        return fcontent

    finally:
        if os.path.exists(temp):
            for root, dirs, files in os.walk(temp, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(temp)

def jfwrite(jarf, nfpath, fcontent):
    temp = "temp_jar_extraction"
    os.makedirs(temp, exist_ok=True)

    try:
        tempfp = os.path.join(temp, os.path.basename(nfpath))
        with open(tempfp, 'w') as f:
            f.write(fcontent)
        with zipfile.ZipFile(jarf, 'a') as jar:
            jar.write(tempfp, arcname=nfpath)

    finally:
        if os.path.exists(temp):
            for root, dirs, files in os.walk(temp, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(temp)

def jfrm(jarf, filetrm):
    temp = "temp_jar_extraction"
    os.makedirs(temp, exist_ok=True)

    try:
        with zipfile.ZipFile(jarf, 'r') as jar:
            jar.extractall(temp)
        filep = os.path.join(temp, filetrm)
        if os.path.exists(filep):
            os.remove(filep)
        with zipfile.ZipFile(jarf, 'w') as jar:
            for root, dirs, files in os.walk(temp):
                for file in files:
                    filep = os.path.join(root, file)
                    rel_path = os.path.relpath(filep, temp)
                    jar.write(filep, rel_path)


    finally:
        if os.path.exists(temp):
            for root, dirs, files in os.walk(temp, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(temp)
######ACTUAL CODE STARTS HERE######
colorama.init()
njf = input(Fore.CYAN+"Select your navine jar file:\n")
print(Fore.MAGENTA+"Testing Jar File..")
if os.path.exists(njf):
    print(Fore.GREEN+"Existing: true")
else:
    print(Fore.RED+"Jarfile did not pass test 'Existing'!")
    input("Press enter to exit")
    sys.exit()
if jfexists(njf,"fabric.mod.json"):
    print(Fore.GREEN+"Is Fabric Mod: true")
else:
    print(Fore.RED+"Jarfile did not pass test 'Is Fabric Mod'!")
    input("Press enter to exit")
    sys.exit()
if jfexists(njf,"navine.mixins.json"):
    print(Fore.GREEN+"Is Navine Client: true")
else:
    print(Fore.RED+"Jarfile did not pass test 'Is Navine Client'!")
    input("Press enter to exit")
    sys.exit()
print(Style.RESET_ALL)
print(Fore.GREEN+"Valid JAR file detected.")
fabricdata = json.loads(jfread(njf,"fabric.mod.json"))
print(Fore.GREEN+"Fabric mod data: "+fabricdata["name"]+" "+fabricdata["version"]+" (mod id: "+fabricdata["id"]+" )")
if jfexists(njf,"modified-by-ncap-DO-NOT-REMOVE.json"):
    ncapdata = json.loads(jfread(njf,"modified-by-ncap-DO-NOT-REMOVE.json"))
    print(Fore.GREEN+"Saved Navine Client Asset Patcher data:\n  Last version used to modify client: "+ncapdata["ncapversion"]+"\n  When was the client modified: "+ncapdata["lastmodified"])
print(Style.RESET_ALL)

choi=input(Fore.CYAN+"Asset to overwrite (valid strings are: 'title screen','uwu module furry mode enabled skin','icon' ):\n")
if not choi in ["title screen","uwu module furry mode enabled skin","icon"]:
    print(Fore.RED+"Invalid asset!")
    input("Press enter to exit")
    sys.exit()
else:
    if choi == "title screen":
            print(Fore.YELLOW+"WARNING: The title screen wallpaper's size must be exactly 3840x2160, otherwise Navine Client might stop working / have bugs")
            imagefilep = input(Fore.CYAN+"Select your input jpg file:\n")
            with open(imagefilep, 'rb') as f:
                icontent = f.read()
            jfrm(njf,"assets/navine/sigma.jpg")
            jifwrite(njf,"assets/navine/sigma.jpg",icontent)
            print(Fore.GREEN+"Written file to assets/navine/sigma.jpg to jarfile")
    if choi == "icon":
            imagefilep = input(Fore.CYAN+"Select your input png file:\n")
            with open(imagefilep, 'rb') as f:
                icontent = f.read()
            jfrm(njf,"assets/navine/icon.png")
            jifwrite(njf,"assets/navine/icon.png",icontent)
            print(Fore.GREEN+"Written file to assets/navine/icon.png to jarfile")
    if choi == "uwu module furry mode enabled skin":
            imagefilep = input(Fore.CYAN+"Select your input skin in a png file:\n")
            with open(imagefilep, 'rb') as f:
                icontent = f.read()
            jfrm(njf,"assets/navine/skin.png")
            jifwrite(njf,"assets/navine/skin.png",icontent)
            print(Fore.GREEN+"Written file to assets/navine/skin.png to jarfile")
jfrm(njf,"modified-by-ncap-DO-NOT-REMOVE.json")
jfwrite(njf,"modified-by-ncap-DO-NOT-REMOVE.json",'{"ncapversion":"'+ncapversion+'","lastmodified":"'+str(datetime.datetime.now())+'"}')
print(Fore.GREEN+"Written NCAP data to jarfile")
input(Fore.MAGENTA+"Press enter to leave app")
