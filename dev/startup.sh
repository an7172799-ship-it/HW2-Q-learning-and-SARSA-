#!/usr/bin/env bash
# dev/startup.sh — begin a development session.
#   1. Pull the latest code from GitHub.
#   2. Print the handover document (HANDOVER.md) so the next dev (human or AI) has context.
#   3. Suggest concrete next actions.
#   4. Run `openspec init` (no-op if already initialised).

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "==> [1/4] git pull (current branch)"
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git pull --ff-only || echo "    (nothing to pull or no upstream set)"
else
  echo "    not a git repo, skipping."
fi

echo ""
echo "==> [2/4] handover document"
if [ -f HANDOVER.md ]; then
  sed 's/^/    /' HANDOVER.md
else
  echo "    HANDOVER.md not found."
fi

echo ""
echo "==> [3/4] suggested next actions"
if [ -d openspec/changes ] && [ -n "$(ls -A openspec/changes 2>/dev/null)" ]; then
  echo "    Open changes awaiting work:"
  for d in openspec/changes/*/; do
    printf "      - %s\n" "$d"
  done
  echo "    -> continue the first unchecked task in its tasks.md"
else
  echo "    No open changes. Consider proposing the next change (NN- prefix)."
fi

echo ""
echo "==> [4/4] openspec init (best-effort)"
if command -v openspec >/dev/null 2>&1; then
  openspec init || true
elif command -v npx >/dev/null 2>&1; then
  npx --yes @fission-ai/openspec@1.1.1 init || true
else
  echo "    openspec / npx not on PATH; skipping. The openspec/ directory is"
  echo "    already scaffolded, so this is not fatal."
fi

echo ""
echo "Ready. Begin development."
