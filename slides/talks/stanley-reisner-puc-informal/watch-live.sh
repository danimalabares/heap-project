#!/bin/bash
# Rebuild live.html whenever the v2 PDF changes. Stop with Ctrl-C or pkill -f watch-live.
PDF=~/github/heap-slides-sr/build/stanley-reisner-puc-informal-v2.pdf
cd "$(dirname "$0")"
last=""
while true; do
  m=$(stat -f %m "$PDF" 2>/dev/null)
  if [ -n "$m" ] && [ "$m" != "$last" ]; then
    sleep 3   # let the compile finish writing
    python3 build-live.py "$PDF" > .watch.log 2>&1 && last=$m
  fi
  sleep 2
done
