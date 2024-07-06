#!/usr/bin/python3
import urllib.request
import ssl
import json
import sys
import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--force", help="force check, even within 24h", action="store_true")
parser.add_argument("-p", "--packages", help="create a new file with mentioned packages", nargs='+')
args = parser.parse_args()

ssl._create_default_https_context = ssl._create_unverified_context

file="packages.json"
curtime=datetime.datetime.now()

if args.packages:
    checktime=curtime + datetime.timedelta(days=-1)
    packagescur = {
        "checktime": str(checktime),
        "packages": []
    }
    for name in args.packages:
        package = {
            "name": name,
            "version": 0
        }
        packagescur["packages"].append(package)
else:
    try:
        with open(file, "r") as f:
            packagescur = json.load(f)
        f.close()
    except FileNotFoundError:
        print(f"Error loading file {file}. Specify packages to create the file")
        sys.exit(2)
    except:
        print(f"Unknown error occured:")
        print(sys.exc_info())
        sys.exit(2)

checktime=datetime.datetime.fromisoformat(packagescur["checktime"])
if args.force or (curtime-checktime).days > 0:
    packagesnew = {
        "checktime": str(datetime.datetime.now()),
        "packages": []
    }
    for package in packagescur["packages"]:
        link = "https://community.chocolatey.org/packages/" + package["name"]
        try:
            with urllib.request.urlopen(link) as response:
                body = str(response.read())
                
                searchstr = '<td class="version"   title="Latest Version"  >'
                index = body.find(searchstr)

                buttonbegin = '<button '
                indexbegin = body.rfind(buttonbegin,0,index)
                buttonend = '>'
                indexend = body.find(buttonend,indexbegin) + 1
                buttonstr = body[indexbegin:indexend]

                versionbegin = 'version="'
                indexbegin = buttonstr.find(versionbegin) + len(versionbegin)
                versionend = '"'
                indexend = buttonstr.find(versionend,indexbegin)
                version=buttonstr[indexbegin:indexend]
        except urllib.error.HTTPError:
            print(f"{package['name']} not found.")
            version = package["version"]
        except:
            print(f"Unknown error occured fetching link { link }:")
            print(sys.exc_info())
            version = package["version"]

        line = {
            "name": package["name"],
            "version": version
        }
        packagesnew["packages"].append(line)

    if packagescur["packages"] != packagesnew["packages"]:
        print("New package versions found.")

    for i in range(len(packagesnew["packages"])):
        if packagesnew["packages"][i] != packagescur["packages"][i]:
            print(packagesnew["packages"][i])
    with open(file, "w", encoding="utf-8") as f:
        json.dump(packagesnew, f, ensure_ascii=False, indent=2)
    f.close()

    if packagescur["packages"] != packagesnew["packages"]:
        input("Press ENTER to exit.")
    else:
        print("No new packages found.")
else:
    print("Last check was within 24 hours ago. No need to check again.")