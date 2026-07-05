---
name: goal
description: Track and advance the standing revenue goal (first $20 of product revenue). Use when the user invokes /goal, asks about goal progress, or asks to work on the money-making goal. Reads the ledger, reports status, then executes the highest-leverage next action.
---

# /goal - Standing revenue goal

The user has a standing goal: **generate $20 in real revenue** through work Claude
does. The strategy chosen (2026-07-05) is a digital product: the Real Estate AI
Lead-Qualification Prompt Pack, sold at $19 via a Stripe Payment Link from
`store.html` on chunkytortoise.github.io.

## On every /goal invocation

1. Read the ledger at `.claude/goals/twenty-dollars.md` (this repo). It is the
   single source of truth for status, blockers, and history.
2. Report to the user in 3 lines or fewer: revenue so far, current blocker,
   next action.
3. Execute the next action from the ledger's "Next actions" list unless the
   user redirects. Ask before anything outward-facing (posting, emailing,
   publishing) unless the ledger records durable permission.
4. Append a dated entry to the ledger's log for whatever you did, update
   "Next actions", commit, and push. An unpushed ledger update does not exist.

## Hard rules (learned from this repo's history)

- **Never publish a buy button with a dead link.** A previous store was pulled
  for exactly this. The store PR stays draft until the user confirms the Stripe
  Payment Link is live and delivers the product.
- Site copy rules: no em-dashes, no AI-slop vocabulary (see the banned-word
  cleanup commits in git history), no fake strikethrough discounts, no invented
  metrics or testimonials. Honest claims only.
- Revenue is only counted when the user confirms a real Stripe payout event.
  Claude never marks the goal complete on its own.
- The paid deliverable (the prompt pack zip) must never be committed to this
  public repo.

## Escalation

If blocked more than two sessions on the same user action, surface it plainly
at the start of the reply instead of working around it.
