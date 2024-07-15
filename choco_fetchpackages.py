#!/usr/bin/python3
import urllib.request
import ssl
import json
import sys
import datetime
import argparse
import glob
import os

parser = argparse.ArgumentParser(
    prog="choco_fetchpages.py",
    description="First create a packages-<nnn>.json file by using the --file and --package parameter. Multiiple files can be created. When running the next time it will fetch the latest version from Chocolaty and update the json files. This can be used as source on different systems to update to the specified version."
)
group = parser.add_argument_group()
parser.add_argument("--force", help="force check, even within 24h", action="store_true")
parser.add_argument("-q", "--quiet", help="quied mode, no input asked.", action="store_true")
group.add_argument("-f", "--file", help="create new package filename. Only specify the suffix and without extension.")
group.add_argument("-p", "--package", help="packages to check", nargs='+')
args = parser.parse_args()

curtime=datetime.datetime.now()
newpackagesfound=False
ssl._create_default_https_context = ssl._create_unverified_context

if args.package and args.file==None:
    print("No filename was specified with --file")
    sys.exit(2)

if args.file:
    files=["packages-" + args.file + ".json"]
else:
    files=glob.glob("packages-*.json")
    if files == []:
        print("No package files found. Please create one with --file and --package")

for file in files:
    if args.package:
        checktime=curtime + datetime.timedelta(days=-1)
        packagescur = {
            "checktime": str(checktime),
            "packages": []
        }
        for name in args.package:
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
            print(f"Error loading file { file }. Specify --file and --package to create the file")
            sys.exit(2)
        except json.decoder.JSONDecodeError:
            print(f"Skipping { file } as it is incorrect and can't be loaded.")
            continue
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
            print(f"New package versions found for { file }.")
            newpackagesfound=True
        else:
            print(f"No new packages found for { file }.")

        for i in range(len(packagesnew["packages"])):
            if packagesnew["packages"][i] != packagescur["packages"][i]:
                print(packagesnew["packages"][i])
        with open(file, "w", encoding="utf-8") as f:
            json.dump(packagesnew, f, ensure_ascii=False, indent=2)
        f.close()
    else:
        print(f"Last check for { file } was within 24 hours ago. No need to check again.")

if args.quiet==False and newpackagesfound==True:
    input("Press ENTER to open explorer.")
    os.startfile(os.getcwd())
