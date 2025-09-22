#!/bin/bash
set -e

PATH=$(pwd)
VENV_PATH="$PATH/venv"

if [ -d "$VENV_PATH" ]; then
    if [ -d "$VENV_PATH/Scripts" ]; then
        source "$VENV_PATH/Scripts/activate"
    elif [ -d "$VENV_PATH/bin" ]; then
        source "$VENV_PATH/bin/activate"
    fi
fi
