# Closing tables

The format every plain-mode answer ends with.

This is the part the reader actually uses. After a long explanation they want two things: where
things stand, and what now.

Use a table when there are **three or more points**, or **two or more next steps**. Below that a
table is noise and one sentence will do. A table beats prose when the reader has to compare or scan.
Prose beats a table when you have one thing to say.

**Status:**

| Item | Status | What this means |
| --- | --- | --- |
| Login flow | ✅ Works | Tested with three accounts |
| Mail sending | ⚠️ Watch | Works, but the API key expires on 14 August |
| Payments | ❌ Failed | Stripe returns a 403, the key looks wrong |

Status values: ✅ done · ⚠️ watch · ❌ failed · ⏳ running · ⏭️ skipped

The table has to be honest. If something failed or was skipped, put that in. A status table that is
all green is worse than no table, because the reader stops looking for themselves.

**Next steps:**

| # | What | Who | Blocking |
| --- | --- | --- | --- |
| 1 | Replace the Stripe key in `.env` | Tim | Yes, payment is down |

**Open choices** (only when there is genuinely something to choose):

| Choice | Options | My advice |
| --- | --- | --- |

Leave a table out if it would be empty. No "n/a" rows.
