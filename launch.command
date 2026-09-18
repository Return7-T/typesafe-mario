#!/bin/zsh
set -eu
cd "${0:A:h}"
if [[ -f .env ]]; then
  set -a
  source .env
  set +a
fi
if [[ -n "${OPENROUTER_API_KEY:-}${TYPESAFE_API_KEY:-}" ]]; then
  policy=typesafe
else
  policy=heuristic
  print '尚未配置 TYPESAFE_API_KEY，启动离线规则策略演示。'
fi
exec .venv/bin/typesafe-mario play --policy "$policy" --display dashboard "$@"
