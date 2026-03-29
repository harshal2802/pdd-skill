#!/usr/bin/env bash
# Test script for hooks/hooks.json session-start hook
# Verifies all detection cases across new (pdd/) and legacy layouts

set -uo pipefail

HOOK_CMD=$(python3 -c "import json,sys; print(json.load(open('hooks/hooks.json'))['hooks'][0]['hooks'][0]['command'])")

pass=0
fail=0

run_test() {
  local name="$1"
  local dir="$2"
  local expected="$3"
  local actual
  actual=$(cd "$dir" && eval "$HOOK_CMD" 2>&1) || true

  if [[ "$actual" == *"$expected"* ]]; then
    echo "PASS: $name"
    pass=$((pass + 1))
  else
    echo "FAIL: $name"
    echo "  expected to contain: $expected"
    echo "  got: $actual"
    fail=$((fail + 1))
  fi
}

# --- Test 1: New layout with project.md that has Last updated ---
tmp=$(mktemp -d)
mkdir -p "$tmp/pdd/context"
echo "Last updated: 2026-03-29" > "$tmp/pdd/context/project.md"
run_test "new layout, project.md with date" "$tmp" \
  "PDD context exists. Last updated: 2026-03-29"
rm -rf "$tmp"

# --- Test 2: New layout with project.md without Last updated ---
tmp=$(mktemp -d)
mkdir -p "$tmp/pdd/context"
echo "Some content, no date" > "$tmp/pdd/context/project.md"
run_test "new layout, project.md without date" "$tmp" \
  "PDD context exists but has no Last updated date"
rm -rf "$tmp"

# --- Test 3: Legacy layout with project.md that has Last updated ---
tmp=$(mktemp -d)
mkdir -p "$tmp/context"
echo "Last updated: 2026-01-15" > "$tmp/context/project.md"
run_test "legacy layout, project.md with date" "$tmp" \
  "PDD context exists (legacy layout). Last updated: 2026-01-15"
rm -rf "$tmp"

# --- Test 4: Legacy layout with project.md without Last updated ---
tmp=$(mktemp -d)
mkdir -p "$tmp/context"
echo "Some content, no date" > "$tmp/context/project.md"
run_test "legacy layout, project.md without date" "$tmp" \
  "PDD context exists (legacy layout) but has no Last updated date"
rm -rf "$tmp"

# --- Test 5: New layout, pdd/prompts exists but no project.md ---
tmp=$(mktemp -d)
mkdir -p "$tmp/pdd/prompts"
run_test "new layout, missing project.md" "$tmp" \
  "PDD project detected but pdd/context/project.md is missing"
rm -rf "$tmp"

# --- Test 6: New layout, pdd/context dir exists but no project.md ---
tmp=$(mktemp -d)
mkdir -p "$tmp/pdd/context"
run_test "new layout, pdd/context dir only, no project.md" "$tmp" \
  "PDD project detected but pdd/context/project.md is missing"
rm -rf "$tmp"

# --- Test 7: Legacy layout, prompts/ exists but no project.md ---
tmp=$(mktemp -d)
mkdir -p "$tmp/prompts"
run_test "legacy layout, missing project.md (prompts/ only)" "$tmp" \
  "PDD project detected (legacy layout) but context/project.md is missing"
rm -rf "$tmp"

# --- Test 8: Legacy layout, context/ dir exists but no project.md ---
tmp=$(mktemp -d)
mkdir -p "$tmp/context"
run_test "legacy layout, missing project.md (context/ dir only)" "$tmp" \
  "PDD project detected (legacy layout) but context/project.md is missing"
rm -rf "$tmp"

# --- Test 9: Non-PDD project (empty dir) — no output ---
tmp=$(mktemp -d)
actual=$(cd "$tmp" && eval "$HOOK_CMD" 2>&1) || true
if [[ -z "$actual" ]]; then
  echo "PASS: non-PDD project, no output"
  pass=$((pass + 1))
else
  echo "FAIL: non-PDD project, no output"
  echo "  expected: (empty)"
  echo "  got: $actual"
  fail=$((fail + 1))
fi
rm -rf "$tmp"

# --- Test 10: Both layouts exist — new layout takes priority ---
tmp=$(mktemp -d)
mkdir -p "$tmp/pdd/context" "$tmp/context"
echo "Last updated: 2026-03-29" > "$tmp/pdd/context/project.md"
echo "Last updated: 2025-01-01" > "$tmp/context/project.md"
run_test "both layouts exist, new layout wins" "$tmp" \
  "PDD context exists. Last updated: 2026-03-29"
rm -rf "$tmp"

# --- Summary ---
echo ""
echo "Results: $pass passed, $fail failed"
if [[ $fail -gt 0 ]]; then
  exit 1
fi
