#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 3 ]]; then
  echo "usage: $0 WORKSPACE OUTPUT CALIBRATION_SCRIPT" >&2
  exit 2
fi

workspace=$1
output=$2
calibration_script=$3
model_key=""

for pid in $(pgrep -f 'vllm|api_server' 2>/dev/null || true); do
  if [[ -r "/proc/$pid/environ" ]]; then
    model_key=$(tr '\0' '\n' < "/proc/$pid/environ" | sed -n 's/^VLLM_API_KEY=//p' | head -1)
    [[ -n "$model_key" ]] && break
  fi
done

if [[ -z "$model_key" ]] && command -v docker >/dev/null 2>&1; then
  for container_id in $(docker ps -q 2>/dev/null || true); do
    model_key=$(docker inspect --format '{{range .Config.Env}}{{println .}}{{end}}' "$container_id" 2>/dev/null | sed -n 's/^VLLM_API_KEY=//p' | head -1)
    [[ -n "$model_key" ]] && break
  done
fi

if [[ -z "$model_key" ]]; then
  echo "GX-local model credential source was not found" >&2
  exit 44
fi

export VLLM_API_KEY="$model_key"
cd "$workspace"
python3 "$calibration_script" --output "$output" --timeout-seconds 900
