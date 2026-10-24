#!/usr/bin/env bash
# Abre, actualiza o cierra el issue de un chequeo semanal según su código de salida.
# Uso: scripts/issue_reporte.sh <label> <titulo> <codigo> <reporte.md>
#   codigo 0 = todo bien (cierra el issue abierto), 1 = problemas (abre o actualiza),
#   otro = el chequeo mismo falló (no toca issues y falla el job).
# Requiere GH_TOKEN y, en Actions, GITHUB_SERVER_URL/GITHUB_REPOSITORY/GITHUB_RUN_ID.
set -euo pipefail

label="$1"; titulo="$2"; codigo="$3"; reporte="$4"
run_url="${GITHUB_SERVER_URL:-https://github.com}/${GITHUB_REPOSITORY:-kvothesson/ar-plugins}/actions/runs/${GITHUB_RUN_ID:-}"
hoy=$(date -u +%F)

gh label create "$label" --color d73a4a --description "$titulo (chequeo automático)" --force
abierto=$(gh issue list --label "$label" --state open --json number --jq '.[0].number // empty')

if [ "$codigo" = "1" ]; then
  printf '\n[Corrida del chequeo](%s)\n' "$run_url" >> "$reporte"
  if [ -n "$abierto" ]; then
    gh issue edit "$abierto" --body-file "$reporte"
    gh issue comment "$abierto" --body "Sigue al $hoy. Reporte actualizado arriba."
  else
    gh issue create --title "$titulo" --label "$label" --body-file "$reporte"
  fi
elif [ "$codigo" = "0" ]; then
  if [ -n "$abierto" ]; then
    gh issue close "$abierto" --comment "Resuelto al $hoy. [Corrida]($run_url)"
  fi
else
  echo "::error::El chequeo falló por otra razón (código $codigo)"
  exit 1
fi
