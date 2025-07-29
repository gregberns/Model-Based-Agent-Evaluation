#!/bin/bash
# scripts/run_plugin.sh

PLUGIN=$1
PLAYBOOK=$2
BUG_DESC=$3

if [ -z "$PLUGIN" ] || [ -z "$PLAYBOOK" ]; then
    echo "Usage: ./scripts/run_plugin.sh <plugin_name> <playbook_name> [bug_description]"
    exit 1
fi

CMD=".venv/bin/python -m packages.framework $PLUGIN $PLAYBOOK --hitl"
if [ -n "$BUG_DESC" ]; then
    CMD="$CMD --bug \"$BUG_DESC\""
fi

echo "Executing: $CMD"
eval $CMD
