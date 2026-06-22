# Handoff — move "Inbox Constellation" into its own repo

This note has everything needed to recreate the email-dashboard project in a
fresh repo from a new Claude Code session. Copy the prompt below into that
session.

## Source location (where the files live now)

- **Repo:** `dancynamon/FileDiff`
- **Branch:** `claude/email-dashboard-platform-links-awmys9`
- **Path:** `email-dashboard/`
- **Files:** `index.html`, `data.js`, `README.md`, `split-out.sh`

## Steps

1. Create an empty **private** repo named `inbox-constellation` (github.com/new).
   Initialize it with a README so it's not empty.
2. Start a new Claude Code session pointed at `inbox-constellation`.
3. Paste the prompt below.

## Prompt to paste into the new session

> Copy the project files from `dancynamon/FileDiff`, branch
> `claude/email-dashboard-platform-links-awmys9`, folder `email-dashboard/`,
> into this repo. The files are `index.html`, `data.js`, `README.md`, and
> `split-out.sh`. Recreate them at the repo root (drop the `email-dashboard/`
> prefix), then commit and push to `main`. If you can't read the source repo
> because it's out of scope, use the repo-list/add-repo tools to add
> `dancynamon/FileDiff` as a read source first; if that's not possible, ask me
> to paste the file contents.

## What this project is

A single-file dashboard that mimics an email inbox and visually wires each
email to related records on connected platforms (QuickBooks, HubSpot CRM,
Google Drive, Slack) using SVG connectors. Sample-data prototype; see
`README.md` for the roadmap to live data.
