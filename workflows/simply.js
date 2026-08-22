export const meta = {
  name: 'simply',
  description: 'Turn a folder of strategy documents into one simple strategy artifact',
  whenToUse: 'When you have a folder of strategy material and want one plain-language page out of it',
  phases: [
    { title: 'Spec',     detail: 'inventory the folder and derive the question' },
    { title: 'Panel',    detail: 'four independent angles read the material' },
    { title: 'Plan',     detail: 'forced ranking to exactly three must-solve' },
    { title: 'Flatten',  detail: 'rewrite at flatten level L1' },
    { title: 'Verify',   detail: 'three scripts, then the one check that is judgement' },
    { title: 'Artifact', detail: 'render two HTML pages, then check them' },
  ],
}

// This file holds wiring only. Every prompt, rule and brief lives in markdown
// under skills/. Change how an agent thinks by editing markdown, never this file.

// One trailing slash, always, so `${folder}compass.md` cannot become `acmecompass.md`.
const given = typeof args === 'string' ? args : (args && args.folder) || './material/'
const base = given.replace(/\/+$/, '')
const folder = base + '/'
const slug = (base.split('/').pop() || 'run').toLowerCase().replace(/[^a-z0-9]+/g, '-')

// Where the plugin's own files live. The skill passes this in, because
// ${CLAUDE_PLUGIN_ROOT} is substituted in skill markdown and not in this script.
// Running from a clone rather than an install, the skill has nothing to pass and '.' is right.
const passed = String((args && args.root) || '.')
const root = (passed.includes('CLAUDE_PLUGIN_ROOT') ? '.' : passed).replace(/\/+$/, '')

// A second run must not quietly overwrite the first. The stamp comes from outside because the
// runtime forbids Date.now(), which would break resume. Same args in, same path out, so
// resumeFromRunId still lands where the first attempt did.
// Stripped to date characters: it becomes a path segment, and a stamp carrying ../ would write
// outside runs/.
const stamp = String((args && args.stamp) || '').replace(/[^0-9A-Za-z-]/g, '').slice(0, 32)
const out = stamp ? `runs/${slug}/${stamp}` : `runs/${slug}`
const R = `${root}/skills/simply/references`

// Only the steps whose job is to read the source get the material folder. The rest work from the
// numbered files their step names. Measured on the first run, every agent read
// the folder and each took a comparable bite, so the flat token profile is this line, not the
// fan-out.
const brief = (task, reads = 'files') => `You are one agent in a Simply Strategy run.
Read ${R}/house-rules.md first. It applies to everything you write.

The plugin root is \`${root}\`. Where a reference file writes {root}, that is the value. Where it
writes a bare skills/, scripts/, templates/ or design/ path, prefix it with the same root.

${reads === 'material'
  ? `The material is in ${folder}. The intake is ${folder}compass.md.`
  : reads === 'compass'
  ? `The intake is ${folder}compass.md and your step needs it. The rest of ${folder} is the source
material, which the numbered files already carry. Read the intake, not the source.`
  : `Your inputs are the files your step names, which already hold what the material said. Do not
open ${folder}. If you find yourself needing it, say so in your output instead.`}
Output goes to ${out}/, which is relative to the working directory and not to the plugin root.
${task}
You own the files this step names. Write nothing else. Return one line: the path you wrote.`

log(`material: ${folder} · output: ${out} · plugin: ${root}`)
if (!stamp) log('no stamp was given, so this run overwrites any earlier run on this folder')

phase('Spec')
await agent(brief(`Your step is "1 · spec" in ${R}/pipeline.md. Follow it and write ${out}/01-spec.md.`, 'material'),
  { label: 'spec', phase: 'Spec' })

phase('Panel')
const ANGLES = ['substance', 'contradict', 'compass', 'attack']
await parallel(ANGLES.map(a => () =>
  agent(brief(`You are the "${a}" angle. Read ${R}/angles.md and follow the "${a}" section only.
Read ${out}/01-spec.md. You cannot see the other angles, which is deliberate.
Write ${out}/02-${a}.md.`, 'material'), { label: a, phase: 'Panel' })))

phase('Plan')
await agent(brief(`Your step is "3 · plan" in ${R}/pipeline.md. Read ${out}/01-spec.md and all four
${out}/02-*.md files. Run the tension check first, then the forced ranking.
Write ${out}/03-plan.md.`, 'compass'), { label: 'plan', phase: 'Plan' })

phase('Flatten')
await agent(brief(`Your step is "4 · flatten" in ${R}/pipeline.md. Load ${root}/skills/flatten/SKILL.md
and read ${root}/skills/flatten/references/before-after.md before you start.
Read ${out}/03-plan.md. Write ${out}/04-plain.md.`), { label: 'flatten', phase: 'Flatten' })

phase('Verify')
// Was three reviewers and a coordinator. Two of those reviewers were doing a
// lookup, and scripts do lookups better: on the first full run the invented
// reviewer passed a file that check_facts.py found nine untraced figures in.
// One agent now runs the checks and does the one job that is judgement.
await agent(brief(`Your step is "5 · verify" in ${R}/pipeline.md. Run the three checks it names,
fix what they report, then check both fidelity hops. Read ${out}/03-plain.md if it exists, the four
${out}/02-*.md and ${out}/04-plain.md.
This step owns two files. Revise ${out}/04-plain.md and write ${out}/05-verdict.md.`, 'material'),
  { label: 'verify', phase: 'Verify' })

const artifact = await agent(brief(`Your step is "6 · artifact" in ${R}/pipeline.md.
Read ${R}/output-structure.md and ${root}/design/DESIGN.md first.

You build two files from two sets of inputs, and the split is the point of this step. The page
carries the finding, the log carries the chain.

The page is ${out}/04-plain.md.
The log is ${out}/01-spec.md for what was read and what is missing, the four ${out}/02-*.md for
which angle found what, ${out}/03-plan.md for what was demoted and why, and ${out}/05-verdict.md for
what was fixed and what shipped with a flag. Surface those. Do not copy the page into the log, and
do not move evidence onto the page to make it look supported.

Fill ${root}/templates/artifact.html and ${root}/templates/reasoning.html.
This step owns two files. Write ${out}/simple-strategy-artifact.html and ${out}/reasoning.html.
Self-contained, black and white.
Then run: python3 ${root}/scripts/check_artifact.py ${out}/ --material ${folder}
You pass that folder to the checker. You do not read it yourself.
The flag is not optional. Without it the pointer check does not run, and a page citing a document
that does not exist passes. It must exit 0. Fix what it reports and run it again.
Return the final check table.`, 'compass'),
  { label: 'artifact', phase: 'Artifact' })

return { slug, folder, artifact: `${out}/simple-strategy-artifact.html`, reasoning: `${out}/reasoning.html` }
