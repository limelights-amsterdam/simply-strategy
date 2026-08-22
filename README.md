# simply-strategy

Explain any strategy like I'm 5.

```
/simply-strategy ./material/acme/
```

Point it at a folder of strategy documents. Out comes one HTML page with big pictures and very few
words that tells someone who knows nothing what the strategy actually says. If the documents contain
no decision, the page says that. It never invents a number.

## Install

```
/plugin marketplace add limelights-amsterdam/simply-strategy
/plugin install simply-strategy
```

Installed as a plugin the skill is namespaced: `/simply-strategy:simply-strategy`. From a clone, one
symlink instead, and it answers to `/simply-strategy` on its own:

```
ln -s "$PWD/skills/simply-strategy" ~/.claude/skills/simply-strategy
```

## What it is not for

Writing the strategy. This explains one that already exists.
