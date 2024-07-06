# choco
Scripts that could be useful using Chocolatey.

## choco_fetchpackages.py
Create a json file with packages and version you want to update. Arguments will be handled as packages and will overwrite the packages.json file.
usage: choco_fetchpackages.py [-h] [--force] [-q] [-f FILE] [-p PACKAGE [PACKAGE ...]]

optional arguments:
  -h, --help            show this help message and exit
  --force               force check, even within 24h
  -q, --quiet           quied mode, no input asked.

  -f FILE, --file FILE  create new package filename. Only specify the suffix and without extension.
  -p PACKAGE [PACKAGE ...], --package PACKAGE [PACKAGE ...]
                        packages to check

## choco_upgrade.ps1
Upgrade packages from packages.json with specified version using choco.
