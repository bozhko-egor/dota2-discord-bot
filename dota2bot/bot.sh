#!/bin/sh


until python3 bot.py; do
    echo "Dota Bot crashed with exit code $?.  Respawning.." >&2
    sleep 1
done
