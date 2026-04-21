#!/usr/bin/env bash
# dev/ending.sh — wrap up a development session.
#   1. Validate open changes: every task in tasks.md must be ticked.
#   2. Archive any fully-complete change (merge its delta specs into openspec/specs/).
#   3. Rewrite HANDOVER.md for the next development iteration.
#   4. Commit and push to GitHub.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "==> [1/4] validate tasks.md completeness"
incomplete_changes=()
if [ -d openspec/changes ]; then
  for change_dir in openspec/changes/*/; do
    [ -d "$change_dir" ] || continue
    tasks_file="$change_dir/tasks.md"
    [ -f "$tasks_file" ] || continue
    if grep -Eq '^\s*-\s+\[\s\]' "$tasks_file"; then
      echo "    UNFINISHED: $change_dir"
      incomplete_changes+=("$change_dir")
    else
      echo "    OK        : $change_dir"
    fi
  done
fi

echo ""
echo "==> [2/4] archive fully-complete changes"
if [ -d openspec/changes ]; then
  for change_dir in openspec/changes/*/; do
    [ -d "$change_dir" ] || continue
    tasks_file="$change_dir/tasks.md"
    [ -f "$tasks_file" ] || continue
    if grep -Eq '^\s*-\s+\[\s\]' "$tasks_file"; then
      echo "    skip (incomplete): $change_dir"
      continue
    fi
    # Merge delta specs into openspec/specs/. The delta file is authoritative.
    if [ -d "$change_dir/specs" ]; then
      for cap_dir in "$change_dir"/specs/*/; do
        [ -d "$cap_dir" ] || continue
        cap_name="$(basename "$cap_dir")"
        mkdir -p "openspec/specs/$cap_name"
        if [ -f "$cap_dir/spec.md" ]; then
          cp "$cap_dir/spec.md" "openspec/specs/$cap_name/spec.md"
          echo "    merged    : $cap_dir -> openspec/specs/$cap_name/spec.md"
        fi
      done
    fi
    # Mark as archived in-place rather than deleting (so history is visible).
    touch "$change_dir/ARCHIVED"
    echo "    archived  : $change_dir"
  done
fi

echo ""
echo "==> [3/4] rewrite HANDOVER.md"
next_num=1
if [ -d openspec/changes ]; then
  for d in openspec/changes/*/; do
    [ -d "$d" ] || continue
    name="$(basename "$d")"
    num="${name%%-*}"
    case "$num" in
      ''|*[!0-9]*) ;;
      *) [ "$num" -ge "$next_num" ] && next_num=$((num + 1)) ;;
    esac
  done
fi
printf -v next_num_pad "%02d" "$next_num"

cat > HANDOVER.md <<EOF
# Handover — as of $(date -u +"%Y-%m-%d %H:%M UTC")

## Repo state

Branch: $(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
HEAD  : $(git rev-parse --short HEAD 2>/dev/null || echo "n/a")

## Open changes (tasks.md not yet fully ticked)

$( if [ ${#incomplete_changes[@]} -eq 0 ]; then
     echo "- none"
   else
     for c in "${incomplete_changes[@]}"; do echo "- $c"; done
   fi )

## Next change number

Use prefix **${next_num_pad}-** for the next proposal.

## Suggested next actions

1. Run \`bash dev/startup.sh\`.
2. Read \`openspec/specs/\` for the current source of truth.
3. If you intend a new capability / behaviour, draft \`openspec/changes/${next_num_pad}-<slug>/proposal.md\` first.
4. Implement, then run \`bash dev/ending.sh\` to archive and push.
EOF
echo "    wrote HANDOVER.md"

echo ""
echo "==> [4/4] commit and push"
git add -A
if git diff --cached --quiet; then
  echo "    nothing to commit."
else
  git commit -m "chore: end-of-session wrap (openspec archive + handover update)"
fi
if git remote get-url origin >/dev/null 2>&1; then
  git push
else
  echo "    no 'origin' remote configured; skipping push."
fi

echo ""
echo "Wrap complete."
