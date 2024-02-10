import json
import zipfile
import os
import sys
import colorama
import datetime
from colorama import Fore, Back, Style
log=""
appstart=str(datetime.datetime.now())
ncapversion="v0.0.2"

def logadd(content):
    global log
    log = log + content + "\n"
    with open("ncaplog-"+appstart.replace(":","-").split(".")[0]+".log","w") as f:
        f.write(log)

    
def jbfwrite(jarf, imagefp, icontent):
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

def jfremove(jarf, filetrm):
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
colorama.just_fix_windows_console()
njf = input(Fore.CYAN+"Select your navine jar file:\n")
logadd("User selected jarfile "+njf)
print(Fore.MAGENTA+"Testing Jar File..")
if os.path.exists(njf):
    print(Fore.GREEN+"Existing: true")
    logadd("Jarfile passed test 'Existing'")
else:
    print(Fore.RED+"Jarfile did not pass test 'Existing'!")
    logadd("Jarfile didn't pass test 'Existing'")
    input("Press enter to exit")
    sys.exit()
if jfexists(njf,"fabric.mod.json"):
    print(Fore.GREEN+"Is Fabric Mod: true")
    logadd("Jarfile passed test 'Is Fabric Mod'")
else:
    logadd("Jarfile didn't pass test 'Is Fabric Mod'")
    print(Fore.RED+"Jarfile did not pass test 'Is Fabric Mod'!")
    input("Press enter to exit")
    sys.exit()
if jfexists(njf,"navine.mixins.json"):
    print(Fore.GREEN+"Is Navine Client: true")
    logadd("Jarfile passed test 'Is Navine Client'")
else:
    logadd("Jarfile didn't pass test 'Is Navine Client'")
    print(Fore.RED+"Jarfile did not pass test 'Is Navine Client'!")
    input("Press enter to exit")
    sys.exit()
if jfexists(njf,"assets/navine/sigma.jpg"):
    print(Fore.GREEN+"Has Navine Assets: true")
    logadd("Jarfile passed test 'Has Navine Assets'")
else:
    logadd("Jarfile didn't pass test 'Has Navine Assets'")
    print(Fore.RED+"Jarfile did not pass test 'Has Navine Assets'!")
    input("Press enter to exit")
    sys.exit()
print(Style.RESET_ALL)
print(Fore.GREEN+"Valid JAR file detected.")
logadd("Valid JAR file detected")
fabricdata = json.loads(jfread(njf,"fabric.mod.json"))
print(Fore.GREEN+"Fabric mod data: "+fabricdata["name"]+" "+fabricdata["version"]+" (mod id: "+fabricdata["id"]+" )")
logadd("Fabric mod data: "+fabricdata["name"]+" "+fabricdata["version"]+" (mod id: "+fabricdata["id"]+" )")
if jfexists(njf,"modified-by-ncap-DO-NOT-REMOVE.json"):
    ncapdata = json.loads(jfread(njf,"modified-by-ncap-DO-NOT-REMOVE.json"))
    print(Fore.GREEN+"Navine Client Asset Patcher data:\n  Last version used to modify client: "+ncapdata["ncapversion"]+"\n  When was the client modified: "+ncapdata["lastmodified"])
    logadd("Navine Client Asset Patcher data:\n  Last version used to modify client: "+ncapdata["ncapversion"]+"\n  When was the client modified: "+ncapdata["lastmodified"])
print(Style.RESET_ALL)

choi=input(Fore.CYAN+"Asset to overwrite (valid strings are: 'title screen','uwu module furry mode enabled skin','icon' ):\n")
logadd("User selected asset: "+choi)
if not choi in ["title screen","uwu module furry mode enabled skin","icon"]:
    print(Fore.RED+"Invalid asset!")
    logadd("User selected invalid asset")
    input("Press enter to exit")
    sys.exit()
else:
    if choi == "title screen":
            print(Fore.YELLOW+"The title screen wallpaper's size must be exactly 3840x2160, otherwise Navine Client might stop working / have bugs")
            logadd("The title screen wallpaper's size must be exactly 3840x2160, otherwise Navine Client might stop working / have bugs")
            imagefilep = input(Fore.CYAN+"Select your input jpg file:\n")
            logadd("User selected image: "+imagefilep)
            with open(imagefilep, 'rb') as f:
                icontent = f.read()
            jfremove(njf,"assets/navine/sigma.jpg")
            jbfwrite(njf,"assets/navine/sigma.jpg",icontent)
            print(Fore.GREEN+"Written "+imagefilep+" to assets/navine/sigma.jpg in jarfile")
            logadd("Written "+imagefilep+" to assets/navine/sigma.jpg in jarfile")
    if choi == "icon":
            imagefilep = input(Fore.CYAN+"Select your input png file:\n")
            logadd("User selected image: "+imagefilep)
            with open(imagefilep, 'rb') as f:
                icontent = f.read()
            jfremove(njf,"assets/navine/icon.png")
            jbfwrite(njf,"assets/navine/icon.png",icontent)
            print(Fore.GREEN+"Written "+imagefilep+" to assets/navine/icon.png in jarfile")
            logadd("Written "+imagefilep+" to assets/navine/icon.png in jarfile")
    if choi == "uwu module furry mode enabled skin":
            imagefilep = input(Fore.CYAN+"Select your input skin in a png file:\n")
            logadd("User selected image: "+imagefilep)
            with open(imagefilep, 'rb') as f:
                icontent = f.read()
            jfremove(njf,"assets/navine/skin.png")
            jbfwrite(njf,"assets/navine/skin.png",icontent)
            print(Fore.GREEN+"Written "+imagefilep+" to assets/navine/skin.png in jarfile")
            logadd("Written "+imagefilep+" to assets/navine/icon.png in jarfile")
jfremove(njf,"modified-by-ncap-DO-NOT-REMOVE.json")
jfwrite(njf,"modified-by-ncap-DO-NOT-REMOVE.json",'{"ncapversion":"'+ncapversion+'","lastmodified":"'+str(datetime.datetime.now())+'"}')
print(Fore.GREEN+"Written NCAP data to jarfile")
logadd("Written NCAP data to modified-by-ncap-DO-NOT-REMOVE.json in jarfile")
input(Fore.MAGENTA+"Press enter to leave app")
logadd("Clean exit")