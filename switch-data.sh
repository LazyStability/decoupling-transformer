#!/usr/bin/env bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

while [[ $# -gt 0 ]]; do
  case $1 in
    -l|--local)
	LOCAL=true
	shift # past value
      ;;
    *)
	break
      ;;
  esac
done


echo "$SCRIPT_DIR"
if [[ $LOCAL ]]; then
	echo "Local run..."
	if [[ -e "$SCRIPT_DIR"/experiments/bachelor-decoupled-wmis/data-local ]]; then
		echo "Save cluster data..."
		mv "$SCRIPT_DIR"/experiments/bachelor-decoupled-wmis/data "$SCRIPT_DIR"/experiments/bachelor-decoupled-wmis/data-cluster
		mv "$SCRIPT_DIR"/experiments/bachelor-decoupled-wmis/data-local "$SCRIPT_DIR"/experiments/bachelor-decoupled-wmis/data
	fi
	uv run "$SCRIPT_DIR"/experiments/bachelor-decoupled-wmis/2025-10-27-compare-chils-ilp.py "$@"
else
	echo "Evaluating cluster run..."
	if [[ -e "$SCRIPT_DIR"/experiments/bachelor-decoupled-wmis/data-cluster ]]; then
		echo "Switch to cluster data..."
		mv "$SCRIPT_DIR"/experiments/bachelor-decoupled-wmis/data "$SCRIPT_DIR"/experiments/bachelor-decoupled-wmis/data-local
		mv  "$SCRIPT_DIR"/experiments/bachelor-decoupled-wmis/data-cluster "$SCRIPT_DIR"/experiments/bachelor-decoupled-wmis/data
	fi
	uv run "$SCRIPT_DIR"/experiments/bachelor-decoupled-wmis/2025-10-27-compare-chils-ilp.py {3..5}
fi

xdg-open "$SCRIPT_DIR"/experiments/bachelor-decoupled-wmis/data/2025-10-27-compare-chils-ilp-eval/test-all.html
notify-send "Experiment done" 'Big text
	Big Text
	Big Text'
