# choco
Scripts that could be useful using Chocolatey.

## choco_fetchpackages.py
Create a json file with packages and latest version you want to update. Multiple json files can be created to use for different systems. Only a single json file can exisit on a system to be used with choco_upgrade.ps1.

usage: choco_fetchpackages.py [-h] [--force] [-q] [-f FILE] [-p PACKAGE [PACKAGE ...]]

optional arguments:  
-h, --help            show this help message and exit  
--force               force check, even within 24h  
-q, --quiet           quied mode, no input asked.  

-f FILE, --file FILE  create new package filename. Only specify the suffix and without extension.  
-p PACKAGE [PACKAGE ...], --package PACKAGE [PACKAGE ...]  packages to check

## choco_upgrade.ps1
Upgrade packages from packages-<nnn>.json with specified version using choco. Only a single json file can exisit in the same folder as the choco_upgrade.ps1 file.
