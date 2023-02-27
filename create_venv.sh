#!/bin/bash

venv_path="/tmp/_venv"
install_packages=0
req_file="requirements.txt"

while [[ $# -gt 0 ]]; do
    case $1 in
        -r)
            install_packages=1
            shift
            ;;
        --)
            shift
            break
            ;;
        -*)
            echo "Error: unrecognized option $1"
            exit 1
            ;;
        *)
            venv_path=$1
            shift
            ;;
    esac
done

virtualenv "$venv_path"
source "$venv_path/bin/activate"
pip install pip -U setuptools wheel

if [ $install_packages -eq 1 ]; then
    while [ "$PWD" != "$HOME" ]; do
        if [ -f "$PWD/$req_file" ]; then
            pip install -r "$PWD/$req_file"
            break
        fi
        cd ..
    done
fi

if [ $# -gt 0 ]; then
    pip install "$@"
fi
