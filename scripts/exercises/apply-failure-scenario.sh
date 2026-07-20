#!/usr/bin/env bash
# Copyright 2026 Ranamicus Technology LLC. All rights reserved.

set -Eeuo pipefail

usage() {
  cat <<'USAGE'
Usage:
  bash scripts/exercises/apply-failure-scenario.sh [--dry-run] <scenario-id>
  bash scripts/exercises/apply-failure-scenario.sh --list
  bash scripts/exercises/apply-failure-scenario.sh --help

Applies a managed Lesson 5.6 failure scenario patch.

Options:
  --dry-run, --check  Verify that the patch can be applied, but do not modify files.
  --list             Show scenario IDs defined in exercises/5.6/scenarios.yml.
  --help             Show this help.

Safety checks:
  - Unknown scenario IDs fail before touching the working tree.
  - The working tree must be clean before applying or dry-running a known scenario.
  - The patch is checked with git apply --unidiff-zero --check before it is applied.
USAGE
}

die() {
  printf 'ERROR: %s\n' "$*" >&2
  exit 1
}

repo_root() {
  git rev-parse --show-toplevel 2>/dev/null || die "Git repository root could not be resolved."
}

scenario_patch() {
  local scenarios_file="$1"
  local wanted_id="$2"
  awk -v wanted_id="$wanted_id" '
    function clean(value) {
      gsub(/^[[:space:]]+|[[:space:]]+$/, "", value)
      gsub(/^["\047]|["\047]$/, "", value)
      return value
    }
    /^[[:space:]]*-[[:space:]]*id:[[:space:]]*/ {
      current = $0
      sub(/^[[:space:]]*-[[:space:]]*id:[[:space:]]*/, "", current)
      in_block = (clean(current) == wanted_id)
    }
    in_block && /^[[:space:]]*patch:[[:space:]]*/ {
      patch = $0
      sub(/^[[:space:]]*patch:[[:space:]]*/, "", patch)
      print clean(patch)
      found = 1
      exit
    }
    END {
      if (!found) {
        exit 1
      }
    }
  ' "$scenarios_file"
}

list_scenarios() {
  local scenarios_file="$1"
  awk '
    function clean(value) {
      gsub(/^[[:space:]]+|[[:space:]]+$/, "", value)
      gsub(/^["\047]|["\047]$/, "", value)
      return value
    }
    /^[[:space:]]*-[[:space:]]*id:[[:space:]]*/ {
      id = $0
      sub(/^[[:space:]]*-[[:space:]]*id:[[:space:]]*/, "", id)
      print clean(id)
    }
  ' "$scenarios_file"
}

ensure_clean_worktree() {
  if ! git diff --quiet; then
    die "Working tree has unstaged changes. Commit, stash, or revert them before applying a scenario."
  fi
  if ! git diff --cached --quiet; then
    die "Index has staged changes. Commit, unstage, or stash them before applying a scenario."
  fi
  if [ -n "$(git ls-files --others --exclude-standard)" ]; then
    die "Working tree has untracked files. Commit, remove, or stash them before applying a scenario."
  fi
}

dry_run=false
list_only=false
scenario_id=""

while [ "$#" -gt 0 ]; do
  case "$1" in
    --help|-h)
      usage
      exit 0
      ;;
    --dry-run|--check)
      dry_run=true
      shift
      ;;
    --list)
      list_only=true
      shift
      ;;
    -*)
      die "Unknown option: $1"
      ;;
    *)
      if [ -n "$scenario_id" ]; then
        die "Only one scenario ID can be specified. first=${scenario_id} extra=$1"
      fi
      scenario_id="$1"
      shift
      ;;
  esac
done

ROOT="$(repo_root)"
cd "$ROOT"

SCENARIOS_FILE="exercises/5.6/scenarios.yml"
[ -f "$SCENARIOS_FILE" ] || die "Scenario file is missing: $SCENARIOS_FILE"

if [ "$list_only" = true ]; then
  list_scenarios "$SCENARIOS_FILE"
  exit 0
fi

[ -n "$scenario_id" ] || die "Scenario ID is required. Use --list to see available scenarios."

patch_path="$(scenario_patch "$SCENARIOS_FILE" "$scenario_id" || true)"
[ -n "$patch_path" ] || die "Unknown scenario ID: ${scenario_id}. Use --list to see available scenarios."
[ -f "$patch_path" ] || die "Patch file for scenario ${scenario_id} is missing: ${patch_path}"

ensure_clean_worktree

if ! git apply --unidiff-zero --check "$patch_path"; then
  die "Patch cannot be applied cleanly. scenario=${scenario_id} patch=${patch_path}"
fi

if [ "$dry_run" = true ]; then
  printf 'Dry-run OK: scenario=%s patch=%s\n' "$scenario_id" "$patch_path"
  printf 'Next: create an exercise branch, apply the patch without --dry-run, then open an exercise PR.\n'
  exit 0
fi

git apply --unidiff-zero "$patch_path"

printf 'Applied scenario: %s\n' "$scenario_id"
printf 'Patch file: %s\n' "$patch_path"
printf 'Next steps:\n'
printf '  1. Review the diff and confirm VERSION matches the exercise issue target_version.\n'
printf '  2. Open an exercise PR with target_version: 0.0.1 and required_final_stage: UT.\n'
printf '  3. Inspect the expected failing job, evidence Artifact, manifest, and pr-ci-gate Summary.\n'
printf '  4. Revert with: git apply --unidiff-zero -R %s\n' "$patch_path"
