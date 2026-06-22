#!/usr/bin/env bash
#
# Split this project out of the FileDiff repo into its own standalone repo.
# Run from your desktop, from INSIDE the email-dashboard/ folder:
#
#     ./split-out.sh
#
# It creates a clean git repo here and, if the `gh` CLI is installed and
# authenticated, creates + pushes a private GitHub repo named below.

set -euo pipefail

REPO_NAME="inbox-constellation"
VISIBILITY="private"   # change to "public" if you want

# Make a fresh git history for just this folder.
git init
git add .
git commit -m "Initial commit: Inbox Constellation email dashboard"

if command -v gh >/dev/null 2>&1; then
  echo "Creating $VISIBILITY GitHub repo '$REPO_NAME' and pushing..."
  gh repo create "$REPO_NAME" --"$VISIBILITY" --source=. --push
  echo "Done."
else
  cat <<EOF

'gh' CLI not found. Create the repo manually, then run:

    git remote add origin git@github.com:<you>/$REPO_NAME.git
    git push -u origin main
EOF
fi
