/**
 * Sample data for the Inbox Constellation dashboard.
 *
 * This is mock data that mimics what a future live version would pull from
 * Gmail + QuickBooks + HubSpot + Google Drive + Slack via their APIs.
 *
 * Each email links to "nodes" on other platforms. The `links` array on an
 * email references node ids; nodes are defined per-platform below.
 */

const PLATFORMS = {
  quickbooks: { name: "QuickBooks",     color: "#2CA01C", short: "QB",  glyph: "$" },
  hubspot:    { name: "HubSpot CRM",    color: "#FF7A59", short: "HS",  glyph: "◆" },
  gdrive:     { name: "Google Drive",   color: "#1A73E8", short: "GD",  glyph: "▦" },
  slack:      { name: "Slack",          color: "#611f69", short: "SL",  glyph: "#" },
};

// Nodes are the individual records on each platform that an email can link to.
const NODES = {
  // ---- HubSpot ----
  "hs-contact-acme":  { platform: "hubspot", type: "Contact", title: "Sarah Lin", subtitle: "VP Operations · Acme Robotics", meta: "Lifecycle: Customer", url: "#" },
  "hs-company-acme":  { platform: "hubspot", type: "Company", title: "Acme Robotics", subtitle: "Manufacturing · 240 employees", meta: "Owner: You", url: "#" },
  "hs-deal-acme":     { platform: "hubspot", type: "Deal",    title: "Acme — Annual Renewal", subtitle: "$48,000 · Stage: Contract Sent", meta: "Close: Jul 2026", url: "#" },
  "hs-contact-nimbus":{ platform: "hubspot", type: "Contact", title: "Marcus Reed", subtitle: "Founder · Nimbus Foods", meta: "Lifecycle: Opportunity", url: "#" },
  "hs-deal-nimbus":   { platform: "hubspot", type: "Deal",    title: "Nimbus — New Order", subtitle: "$12,500 · Stage: Negotiation", meta: "Close: Jun 2026", url: "#" },
  "hs-contact-orbit": { platform: "hubspot", type: "Contact", title: "Priya Nair", subtitle: "Accounts Payable · Orbit Studios", meta: "Lifecycle: Customer", url: "#" },

  // ---- QuickBooks ----
  "qb-inv-1042":  { platform: "quickbooks", type: "Invoice", title: "Invoice #1042", subtitle: "Acme Robotics · $48,000.00", meta: "Status: Sent · Due Jul 15", url: "#" },
  "qb-inv-1039":  { platform: "quickbooks", type: "Invoice", title: "Invoice #1039", subtitle: "Acme Robotics · $4,200.00", meta: "Status: Paid", url: "#" },
  "qb-bill-882":  { platform: "quickbooks", type: "Bill",    title: "Bill #882", subtitle: "Contoso Parts · $9,150.00", meta: "Status: Open · Due Jun 30", url: "#" },
  "qb-inv-1051":  { platform: "quickbooks", type: "Invoice", title: "Invoice #1051", subtitle: "Nimbus Foods · $12,500.00", meta: "Status: Draft", url: "#" },
  "qb-pmt-771":   { platform: "quickbooks", type: "Payment", title: "Payment #771", subtitle: "Orbit Studios · $3,600.00", meta: "Received Jun 18", url: "#" },
  "qb-inv-1033":  { platform: "quickbooks", type: "Invoice", title: "Invoice #1033", subtitle: "Orbit Studios · $3,600.00", meta: "Status: Paid", url: "#" },

  // ---- Google Drive / Sheets ----
  "gd-sheet-acme":  { platform: "gdrive", type: "Sheet", title: "Acme — Renewal Pricing.xlsx", subtitle: "Shared sheet · last edit 2d ago", meta: "Owner: you@aquamentor.com", url: "#" },
  "gd-doc-sow":     { platform: "gdrive", type: "Doc",   title: "Acme SOW 2026.docx", subtitle: "Statement of Work", meta: "Modified Jun 19", url: "#" },
  "gd-sheet-nimbus":{ platform: "gdrive", type: "Sheet", title: "Nimbus Order Plan.xlsx", subtitle: "Line items + margins", meta: "Modified Jun 20", url: "#" },
  "gd-folder-orbit":{ platform: "gdrive", type: "Folder",title: "Orbit Studios /", subtitle: "12 files", meta: "Shared", url: "#" },

  // ---- Slack ----
  "sl-acme":   { platform: "slack", type: "Channel", title: "#acct-acme-robotics", subtitle: "4 unread · 6 members", meta: "Last: Sarah's renewal Q", url: "#" },
  "sl-finance":{ platform: "slack", type: "Channel", title: "#finance-ap", subtitle: "AP approvals", meta: "Bill #882 pending", url: "#" },
  "sl-nimbus": { platform: "slack", type: "Thread",  title: "Nimbus order thread", subtitle: "in #sales", meta: "8 replies", url: "#" },
};

const EMAILS = [
  {
    id: "e1",
    from: "Sarah Lin",
    fromEmail: "sarah.lin@acmerobotics.com",
    company: "Acme Robotics",
    avatarColor: "#6366f1",
    subject: "Re: Annual renewal — ready to sign",
    snippet: "Thanks for the updated pricing. The numbers look good on our end — can you send over the final invoice and SOW so I can route them for signature this week?",
    body: `Hi,

Thanks for the updated pricing. The numbers look good on our end — can you send over the final invoice and SOW so I can route them for signature this week?

A couple of small notes:
• Finance wants the invoice net-30 from issue date.
• Please CC priya@ on the SOW.

Appreciate the quick turnaround.

Best,
Sarah Lin
VP Operations, Acme Robotics`,
    time: "9:14 AM",
    date: "Today",
    unread: true,
    starred: true,
    links: ["hs-contact-acme", "hs-company-acme", "hs-deal-acme", "qb-inv-1042", "gd-sheet-acme", "gd-doc-sow", "sl-acme"],
  },
  {
    id: "e2",
    from: "Marcus Reed",
    fromEmail: "marcus@nimbusfoods.co",
    company: "Nimbus Foods",
    avatarColor: "#0ea5e9",
    subject: "New order — 200 units, need a quote",
    snippet: "We'd like to place a larger order this quarter. Can you put together a quote for 200 units and let me know lead time?",
    body: `Hey,

We'd like to place a larger order this quarter. Can you put together a quote for 200 units and let me know lead time?

If pricing works we'd want to move fast — targeting delivery before end of month.

Thanks,
Marcus Reed
Founder, Nimbus Foods`,
    time: "Yesterday",
    date: "Jun 21",
    unread: true,
    starred: false,
    links: ["hs-contact-nimbus", "hs-deal-nimbus", "qb-inv-1051", "gd-sheet-nimbus", "sl-nimbus"],
  },
  {
    id: "e3",
    from: "Priya Nair",
    fromEmail: "priya@orbitstudios.io",
    company: "Orbit Studios",
    avatarColor: "#10b981",
    subject: "Payment sent — Invoice 1033",
    snippet: "Just a heads up that we've processed payment for invoice 1033. Let me know once it clears on your side.",
    body: `Hi,

Just a heads up that we've processed payment for invoice 1033 ($3,600). Let me know once it clears on your side.

Also — we'll have the next batch of files in the shared folder by Friday.

Best,
Priya Nair
Accounts Payable, Orbit Studios`,
    time: "Jun 18",
    date: "Jun 18",
    unread: false,
    starred: false,
    links: ["hs-contact-orbit", "qb-inv-1033", "qb-pmt-771", "gd-folder-orbit"],
  },
  {
    id: "e4",
    from: "Contoso Parts (Billing)",
    fromEmail: "ar@contosoparts.com",
    company: "Contoso Parts",
    avatarColor: "#f59e0b",
    subject: "Invoice due: Bill #882",
    snippet: "Reminder that bill #882 for $9,150 is due June 30. Please confirm payment scheduling.",
    body: `Hello,

This is a reminder that bill #882 for $9,150.00 is due June 30.

Please confirm payment scheduling at your earliest convenience.

Regards,
Contoso Parts Accounts Receivable`,
    time: "Jun 17",
    date: "Jun 17",
    unread: false,
    starred: false,
    links: ["qb-bill-882", "sl-finance"],
  },
];
