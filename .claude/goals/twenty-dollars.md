# Goal: first $20 of product revenue

**Status**: in progress | **Revenue confirmed**: $0 / $20
**Strategy**: sell the Real Estate AI Lead-Qualification Prompt Pack at $19
via Stripe Payment Link on `store.html`. One sale (plus any tip or a second
sale) clears the goal.

## Current blocker

User must create the Stripe Payment Link and attach the deliverable
(see checklist below), then swap the two `buy.stripe.com/REPLACE_ME` hrefs in
`store.html` and mark the PR ready.

## User checklist (about 10 minutes in Stripe)

1. Stripe Dashboard -> Product catalog -> Add product:
   "Real Estate AI Lead-Qualification Prompt Pack", one-time, $19.
2. Create a Payment Link for it. In the link's After-payment settings, set a
   custom confirmation message containing the download URL for
   `real-estate-ai-prompt-pack-v1.zip` (host the zip anywhere private-ish:
   Google Drive share link, S3, or Gumroad's free hosting). Claude has sent
   you the zip; it must not be committed to this repo.
3. Replace both `https://buy.stripe.com/REPLACE_ME` hrefs in `store.html`
   with the real link.
4. Do one live test purchase yourself, refund it, confirm the download works.
5. Mark the PR ready for review and merge. The page goes live on GitHub Pages.

## Next actions (Claude, in order)

1. If the Stripe link is in place: verify both hrefs, merge readiness, then
   move to distribution: publish the launch copy (drafts already delivered to
   the user) after user approval per outward-facing rule.
2. If revenue > $0 confirmed by user: log it, celebrate briefly, propose
   whether to extend the goal or close it.
3. If blocked on the checklist 2+ sessions: surface the blocker, offer the
   Gumroad-only fallback (Gumroad hosts file delivery and checkout in one,
   removing steps 2 and 4).

## Log

- 2026-07-05: Goal created. Prior art found: a 12-product store.html was pulled
  2026-06-22 for dead Stripe buttons; old Gumroad links unverifiable from this
  environment (network policy blocks gumroad.com). Built v1 of the prompt pack
  (9 files, ~4,800 words), rebuilt store.html as a single-product honest page,
  created this skill + ledger, opened draft PR. Launch copy (LinkedIn/X/email)
  delivered to user out-of-repo. Revenue: $0.
