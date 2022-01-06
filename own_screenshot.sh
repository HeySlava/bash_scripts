#!/bin/sh

FILENAME="note-"$(date +%s)".png"

PROJECTDIR=$(cat ~/code/bash_scripts/own_screenshot.config)/
mkdir -p $PROJECTDIR"img"

SCREENSHOT_PATH=$PROJECTDIR"img/"$FILENAME

TO_CLIPBOARD="./img/"$FILENAME

gnome-screenshot --area --file=$SCREENSHOT_PATH

echo -n $TO_CLIPBOARD | xclip -i -selection clipboard
