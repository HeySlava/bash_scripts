#!/bin/sh

filename="note-"$(date +%s)".png"

project_dir=$(cat /tmp/screenshot_local.config)
mkdir -p $project_dir"/img"

screenshot_path=$project_dir"/img/"$filename


echo $screenshot_path

to_clipboard="./img/"$filename

gnome-screenshot --area --file=$screenshot_path

echo -n $to_clipboard | xclip -i -selection clipboard
