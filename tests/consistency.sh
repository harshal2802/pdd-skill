#!/usr/bin/env bash
set -euo pipefail

FAIL=0
fail() { echo "FAIL: $1"; FAIL=1; }
pass() { echo "OK:   $1"; }

# ── 1. Commands ↔ Copilot prompts parity ──
diff_output=$(diff \
  <(ls commands/ | sed 's/.md//' | sort) \
  <(ls copilot/prompts/ | sed 's/.prompt.md//' | sort) || true)

if [ -n "$diff_output" ]; then
  fail "commands/ and copilot/prompts/ are out of sync:"
  echo "$diff_output"
else
  pass "commands/ ↔ copilot/prompts/ in sync"
fi

# ── 2. Reference files exist ──
for f in frontend backend mobile data-ml devops fullstack library cli-devtools embedded-iot game-dev blockchain security api-platform desktop-gui compiler-lang robotics; do
  [ -f "references/$f.md" ] && pass "references/$f.md" || fail "references/$f.md missing"
done

# ── 3. Copilot README covers all references ──
for f in frontend backend mobile data-ml devops fullstack library cli-devtools embedded-iot game-dev blockchain security api-platform desktop-gui compiler-lang robotics; do
  grep -q "$f.md" copilot/README.md \
    && pass "$f.md in copilot/README.md" \
    || fail "$f.md missing from copilot/README.md setup"
done

# ── 4. Slash command refs in commands/ resolve ──
grep -roh '/project:pdd-[a-z-]*' commands/*.md 2>/dev/null | sort -u | while read -r cmd; do
  target="commands/$(echo "$cmd" | sed 's|/project:||').md"
  [ -f "$target" ] && pass "$cmd → $target" || fail "$cmd → $target not found"
done

# ── 5. Every command file in README ──
for f in $(ls commands/ | sed 's/.md//'); do
  grep -q "$f" README.md \
    && pass "$f in README.md" \
    || fail "$f missing from README.md"
done

# ── 6. Every copilot prompt in copilot README ──
for f in $(ls copilot/prompts/ | sed 's/.prompt.md//'); do
  grep -q "$f" copilot/README.md \
    && pass "$f in copilot/README.md" \
    || fail "$f missing from copilot/README.md"
done

# ── 7. Workflow count sanity ──
# Count numbered workflows in the SKILL.md intro list (e.g. "1. **Scaffold**")
skill_count=$(grep -cE '^[0-9]+\. \*\*' skills/pdd/SKILL.md)
cmd_count=$(ls commands/pdd-*.md | wc -l | tr -d ' ')
# commands include help + status, so cmd_count = skill_count + 2
expected=$((skill_count + 2))
if [ "$cmd_count" -eq "$expected" ]; then
  pass "Workflow count: $skill_count workflows, $cmd_count commands (includes help+status)"
else
  fail "Workflow count mismatch: skills/pdd/SKILL.md has $skill_count, commands/ has $cmd_count (expected $expected)"
fi

echo ""
if [ "$FAIL" -eq 0 ]; then
  echo "All checks passed."
  exit 0
else
  echo "Some checks failed."
  exit 1
fi
