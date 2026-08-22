export const meta = {
  name: 'simply',
  description: 'Turn a folder of strategy documents into one simple strategy artifact',
  whenToUse: 'When you have a folder of strategy material and want one plain-language page out of it',
  phases: [
    { title: 'Spec',     detail: 'inventory the folder and derive the question' },
    { title: 'Panel',    detail: 'four independent angles read the material' },
    { title: 'Plan',     detail: 'forced ranking to exactly three must-solve' },
    { title: 'Flatten',  detail: 'rewrite at flatten level L1' },
    { title: 'Review',   detail: 'still true, actually simple, anything invented' },
    { title: 'Artifact', detail: 'consolidate, then render two HTML pages' },
  ],
}

// This file holds wiring only. Every prompt, rule and brief lives in markdown
// under skills/. Change how an agent thinks by editing markdown, never this file.

// One trailing slash, always, so `${folder}compass.md` cannot become `acmecompass.md`.
const given = typeof args === 'string' ? args : (args && args.folder) || './material/'
const folder = given.replace(/\/+$/, '') + '/'
const slug = (folder.replace(/\/+$/, '').split('/').pop() || 'run').toLowerCase().replace(/[^a-z0-9]+/g, '-')

// Where the plugin's own files live. The skill passes this in, because
// ${CLAUDE_PLUGIN_ROOT} is substituted in skill markdown and not in this script.
// Running from a clone rather than an install, the skill has nothing to pass and '.' is right.
const passed = (args && args.root) || '.'
const root = (!passed || passed.includes('CLAUDE_PLUGIN_ROOT') ? '.' : passed).replace(/\/+$/, '')

const out = `runs/${slug}`
const R = `${root}/skills/simply/references`

const brief = (task) => `You are one agent in a Simply Strategy run.
Read ${R}/house-rules.md first. It applies to everything you write.

The plugin root is \`${root}\`
Every path this run names that starts with skills/, scripts/, templates/ or design/ sits under that
root, including such paths written inside the reference files you are told to read. Prefix them
yourself. Do not go looking for them relative to the working directory.

The material is in ${folder}. The intake is ${folder}compass.md. Output goes to ${out}/, which is
relative to the working directory and not to the plugin root.
${task}
You own the files this step names. Write nothing else. Return one line: the path you wrote.`

log(`material: ${folder} · output: ${out} · plugin: ${root}`)

phase('Spec')
await agent(brief(`Your step is "1 · spec" in ${R}/pipeline.md. Follow it and write ${out}/01-spec.md.`),
  { label: 'spec', phase: 'Spec' })

phase('Panel')
const ANGLES = ['substance', 'contradict', 'compass', 'attack']
await parallel(ANGLES.map(a => () =>
  agent(brief(`You are the "${a}" angle. Read ${R}/angles.md and follow the "${a}" section only.
Read ${out}/01-spec.md. You cannot see the other angles, which is deliberate.
Write ${out}/02-${a}.md.`), { label: a, phase: 'Panel' })))

phase('Plan')
await agent(brief(`Your step is "3 · plan" in ${R}/pipeline.md. Read ${out}/01-spec.md and all four
${out}/02-*.md files. Run the tension check first, then the forced ranking.
Write ${out}/03-plan.md.`), { label: 'plan', phase: 'Plan' })

phase('Flatten')
await agent(brief(`Your step is "4 · flatten" in ${R}/pipeline.md. Load ${root}/skills/simplify/SKILL.md
and read ${root}/skills/simplify/references/before-after.md before you start.
Read ${out}/03-plan.md. Write ${out}/04-plain.md.`), { label: 'flatten', phase: 'Flatten' })

phase('Review')
const REVIEWERS = ['true', 'simple', 'invented']
await parallel(REVIEWERS.map(r => () =>
  agent(brief(`You are the "${r}" reviewer. Read the review table in ${R}/pipeline.md step 5.
Read ${out}/03-plan.md and ${out}/04-plain.md, and the four ${out}/02-*.md files if your brief
needs them. Mark every finding fatal or minor, with its line.
Write ${out}/05-${r}.md.`), { label: r, phase: 'Review' })))

phase('Artifact')
await agent(brief(`Your step is "6 · coordinate" in ${R}/pipeline.md. Read the three ${out}/05-*.md
files. Two or more reviewers calling something fatal is decisive.
This step owns two files, which is the exception in this run. Apply the must-fix list to
${out}/04-plain.md in one round, and write ${out}/05-verdict.md.`),
  { label: 'coordinate', phase: 'Artifact' })

const artifact = await agent(brief(`Your step is "7 · artifact" in ${R}/pipeline.md.
Read ${R}/output-structure.md, ${root}/design/DESIGN.md, ${out}/04-plain.md, ${out}/05-verdict.md
and ${out}/01-spec.md. Fill ${root}/templates/artifact.html and ${root}/templates/reasoning.html.
This step owns two files. Write ${out}/simple-strategy-artifact.html and ${out}/reasoning.html.
Self-contained, black and white.
Then run: python3 ${root}/scripts/check_artifact.py ${out}/
It must exit 0. Fix what it reports and run it again. Return the final check table.`),
  { label: 'artifact', phase: 'Artifact' })

return { slug, folder, artifact: `${out}/simple-strategy-artifact.html`, reasoning: `${out}/reasoning.html` }
