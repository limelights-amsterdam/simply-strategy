# simply-strategy

A Claude Code plugin with one skill, `simply-strategy`: eli5 for strategy documents. The whole skill
is `skills/simply-strategy/SKILL.md`, one instruction and three guards. Keep it that way: no
references, no scripts, no templates. If a rule is worth having it fits in the body; if it does not
fit, it is not worth having.

Do not add a number to the docs that a run did not produce. No em dashes.

```
/simply-strategy ./material/<client>/
```

`material/` and `runs/` are git-ignored.
