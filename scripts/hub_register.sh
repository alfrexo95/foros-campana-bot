#!/usr/bin/env bash
set -u
TOKEN="\${INFRA_HUB_TOKEN:-}"
if [[ -z "$TOKEN" ]]; then
  echo "Hub registration skipped: token not configured"
  exit 0
fi
HUB_URL="\${INFRA_HUB_URL:-https://x402-api-wigc.onrender.com}"
HUB_URL="\${HUB_URL%/}"
AGENT_ID="foros-campana-bot"
CAPABILITIES='["forum.publish.botchan","forum.publish.anystation"]'
AUTH_CONFIG="$(mktemp)"
chmod 600 "$AUTH_CONFIG"
trap 'rm -f "$AUTH_CONFIG"' EXIT
printf 'header = "Authorization: Bearer %s"\n' "$TOKEN" > "$AUTH_CONFIG"

register_status="$(curl --config "$AUTH_CONFIG" --silent --show-error --connect-timeout 3 --max-time 8 -o /dev/null -w '%{http_code}' -H 'Content-Type: application/json' -H 'Accept: application/json' -d "{\"agent_id\":\"\${AGENT_ID}\",\"platform\":\"github-actions\",\"capabilities\":\${CAPABILITIES}}" "\${HUB_URL}/infra/agents/register" 2>/dev/null)" || register_status="000"
if [[ ! "$register_status" =~ ^2[0-9]{2}$ ]]; then
  echo "Hub registration failed non-blocking (status \${register_status})"
  exit 0
fi
heartbeat_status="$(curl --config "$AUTH_CONFIG" --silent --show-error --connect-timeout 3 --max-time 8 -o /dev/null -w '%{http_code}' -H 'Content-Type: application/json' -H 'Accept: application/json' -d '{}' "\${HUB_URL}/infra/agents/\${AGENT_ID}/heartbeat" 2>/dev/null)" || heartbeat_status="000"
if [[ ! "$heartbeat_status" =~ ^2[0-9]{2}$ ]]; then
  echo "Hub heartbeat failed non-blocking (status \${heartbeat_status})"
else
  echo "Hub registration and heartbeat completed (HTTP \${register_status}/\${heartbeat_status})"
fi
exit 0
