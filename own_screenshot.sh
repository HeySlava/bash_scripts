#!/bin/sh

FILENAME="note-"$(date +%s)".png"
NOTEDIR=$(cat screenshot.config)/
COPYFILE=$NOTEDIR$FILENAME.copy
TO_CLIPBOARD="./img/$FILENAME"

gnome-screenshot --file=$FILENAME

cp /home/slava/Pictures/$FILENAME $COPYFILE
rm /home/slava/Pictures/$FILENAME 
echo $TO_CLIPBOARD | xclip -i -selection clipboard
# echo $COPYFILE
