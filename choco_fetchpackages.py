#!/usr/bin/python3
import urllib.request
import ssl
import json
import sys

ssl._create_default_https_context = ssl._create_unverified_context

file="packages.json"

if len(sys.argv) > 1:
    packagescur = []
    for i in range(1,len(sys.argv)):
        package = {
            "name": sys.argv[i],
            "version": 0
        }
        packagescur.append(package)
else:
    try:
        with open(file, "r") as f:
            packagescur = json.load(f)
        f.close()
    except:
        print(f"Error loading file {file}. Specify packages to create the file")
        sys.exit(2)     

packagesnew = []
for package in packagescur:
    link = "https://community.chocolatey.org/packages/" + package['name']

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

    line = {
        "name": package['name'],
        "version": version
    }
    packagesnew.append(line)

if packagescur != packagesnew:
    print("New package versions found:")
    for i in range(len(packagesnew)):
        if packagesnew[i] != packagescur[i]:
            print(packagesnew[i])
    with open(file, "w", encoding="utf-8") as f:
        json.dump(packagesnew, f, ensure_ascii=False, indent=2)
    f.close()
else:
    print("No new packages found.")