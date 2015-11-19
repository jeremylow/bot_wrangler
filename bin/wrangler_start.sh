#!/bin/bash

# Name of the application
NAME="Bot Wrangler"

# Project directory (contains the actual application that we're going to run)
WRANGLERDIR=/home/YOU/bot_wrangler/

# Virtual environment directory
VENVDIR=/home/YOU/.venvs/bot_wrangler

# the user and group the program should run as
USER=YOU
GROUP=YOU
NUM_WORKERS=1

# Activate the virtual environment
source $VENVDIR/bin/activate

# Append the server directory to our python path environment variable.
export PYTHONPATH=$WRANGLERDIR:$PYTHONPATH

# Programs meant to be run under supervisor should not daemonize themselves
# (do not use --daemon). So we'll cd to our server directory and then
# execute the program using the virtualenv's version of python.
cd $WRANGLERDIR

exec $VENVDIR/bin/python wrangler.py