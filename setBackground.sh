#!/bin/bash

python3 himawari.py -o /tmp/himawariBG.png
gsettings set org.gnome.desktop.background picture-uri file:///tmp/himawariBG.png
gsettings set org.gnome.desktop.background picture-options scaled

echo 'Done'
