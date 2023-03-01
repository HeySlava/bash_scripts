#!/bin/bash

venv_path="/tmp/_venv"
install_packages=0
req_file="requirements.txt"
tox=0

while [[ $# -gt 0 ]]; do
    case $1 in
        -py*)
            tox=1
            tox_venv=$1
            break
            ;;
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
        .)
            venv_path='_venv'
            shift
            ;;
        *)
            venv_path=$1
            shift
            ;;
    esac
done

prefix="-"
tox_venv_striped=${tox_venv#"$prefix"}

if [ $tox -eq 1 ]; then
    source ".tox/$tox_venv_striped/bin/activate"
else
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
fi
