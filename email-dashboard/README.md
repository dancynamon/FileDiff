# Inbox Constellation

A dashboard that mimics an email inbox and visually wires each email to the
web-application records it relates to — QuickBooks invoices/bills, HubSpot CRM
contacts/companies/deals, Google Drive sheets/docs, and Slack channels/threads.

Think of it as a lightweight, email-first CRM view: open a message on the left,
and see a "constellation" of every connected platform record on the right, with
curved links drawn from the email to each one.

## Run it

No build step. Just open the file in a browser:

```
email-dashboard/index.html
```

(or serve the folder: `python3 -m http.server` then visit `/email-dashboard/`)

## What's here

| File         | Purpose                                                        |
|--------------|----------------------------------------------------------------|
| `index.html` | The dashboard UI, layout, and SVG connector rendering.         |
| `data.js`    | Sample data — platforms, linked records (nodes), and emails.   |

## How it works

- **`PLATFORMS`** — the connected web apps and their brand colors/icons.
- **`NODES`** — individual records on each platform (an invoice, a deal, a sheet).
- **`EMAILS`** — inbox messages; each has a `links` array of node ids it relates to.

Selecting an email groups its linked nodes by platform and draws bezier wires
from the email card to each record card. Hovering a card isolates its link.

## Roadmap → live data

This is a sample-data prototype to nail the UX first. The same UI can later be
fed by real integrations already available in this workspace:

- **Gmail** → real inbox messages
- **QuickBooks** → match invoices/bills by customer + amount
- **HubSpot** → resolve sender email to contact/company/deal
- **Google Drive** → search files shared with / mentioning the customer
- **Slack** → find the customer's account channel/threads

The matching logic (email ⇄ records) becomes the core engine; the data shape in
`data.js` is the contract the live layer would produce.
