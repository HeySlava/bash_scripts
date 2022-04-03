#!/bin/bash

tmp=$(echo $(date)$IMG_SALT | sha256sum)
HASHED=${tmp:0:10}
FILENAME=$HASHED".png"

IMG_DIR=$HOME/".img-bak/"
mkdir -p $IMG_DIR

SCREENSHOT_PATH=$IMG_DIR$FILENAME

gnome-screenshot --area --file=$SCREENSHOT_PATH

scp $SCREENSHOT_PATH kapitonov:~/.img-bak
TO_CLIPBOARD="https://kapitonov.tech/img/"$FILENAME


echo -n $TO_CLIPBOARD | xclip -i -selection clipboard

