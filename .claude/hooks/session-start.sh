#!/bin/bash
set -euo pipefail

# Only run in Claude Code cloud sessions
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "${CLAUDE_PROJECT_DIR:-.}"

# Dev tools (linter) go into the system Python. Skip if nothing changed.
pyhashes="$(python3 -I -c 'import sysconfig; print(sysconfig.get_path("purelib"))')/.session-start.sha256"
if ! sha256sum --check --status "$pyhashes" 2>/dev/null; then
  rm -f "$pyhashes"
  python3 -m pip install --quiet --break-system-packages --root-user-action=ignore -r requirements-dev.txt
  sha256sum .claude/hooks/session-start.sh requirements-dev.txt > "$pyhashes" || rm -f "$pyhashes"
fi

echo 'export PYTHONDONTWRITEBYTECODE=1' >> "${CLAUDE_ENV_FILE:-/dev/null}"
