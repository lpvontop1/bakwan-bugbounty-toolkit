#!/usr/bin/env bash
# Monitor production game recovery on tab t1. Logs to prod_monitor.log
LOG=/home/z/my-project/scripts/prod_monitor.log
echo "monitor start $(date +%H:%M:%S)" >> $LOG
for i in $(seq 1 40); do
  agent-browser tab t1 >/dev/null 2>&1
  agent-browser reload >/dev/null 2>&1
  sleep 14
  OUT=$(agent-browser snapshot -i 2>&1)
  if echo "$OUT" | grep -q "Coba lagi"; then
    echo "$(date +%H:%M:%S) try=$i DOWN" >> $LOG
  elif echo "$OUT" | grep -qE "Ranked Online|Train Latihan|Masuk / Daftar"; then
    echo "$(date +%H:%M:%S) try=$i UP" >> $LOG
    echo "GAME_UP" >> $LOG
    exit 0
  else
    echo "$(date +%H:%M:%S) try=$i UNKNOWN: $(echo "$OUT" | tail -3 | tr '\n' ' ')" >> $LOG
  fi
  sleep 75
done
echo "monitor end $(date +%H:%M:%S)" >> $LOG
