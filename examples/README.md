# A worked example

One run's output, anonymised. Open `simple-strategy-artifact.html` in a browser.

The names, figures and slide numbers come from a real run on a real folder, with
the client's identity removed. The shape is exactly what the pipeline produces.

| | |
|---|---|
| Words on the page | 646 |
| Reading time | 3.2 minutes at 200 a minute |
| Figures | five, from the six in `design/DESIGN.md` |
| Source pointers | on every claim |

The page carries the finding. `reasoning.html` carries the evidence: what it
read, what it threw away, where it is unsure, and what shipped with a flag.

Both files validate against the checker, which is the point of keeping them here:

```
python3 scripts/check_artifact.py examples/
```

The file names match what a run writes, so the checker finds the pair the same
way it does in `runs/<slug>/<stamp>/`. If a change to the templates breaks the contract,
this fails in CI before anyone renders a real one.
