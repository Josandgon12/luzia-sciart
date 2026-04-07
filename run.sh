#!/bin/bash

# Auto-detect script directory
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cd "$SCRIPT_DIR/luzia" || exit

while true
do
  # Execute with memory limits
  systemd-run --scope -p MemoryMax=500M -p MemorySwapMax=10M python3 luzia.py
done
