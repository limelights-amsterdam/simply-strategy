# simply-strategy

A Claude Code plugin with one skill, `simply-strategy`: eli5 for strategy documents. The skill is
`skills/simply-strategy/SKILL.md`, one instruction and three guards, plus four short references
under `skills/simply-strategy/references/` that say how (material, decision, words, page) and one
template, `skills/simply-strategy/assets/page.html`, that fixes the shape of the page. Keep it that
way: no scripts, no second template, no fifth reference unless a run showed the page needs it. If
a rule is worth having it fits in one of those six files; if it does not fit, it is not worth
having.

Do not add a number to the docs that a run did not produce. No em dashes.

```
/simply-strategy ./material/<client>/
```

`material/` and `runs/` are git-ignored.
