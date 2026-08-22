export const meta = {
  name: 'ablation-2step',
  description: 'Spec then flatten, nothing else. Measures what the panel and the reviewers buy',
  whenToUse: 'Only for the ablation. The real run is /simply',
  phases: [{ title: 'Spec' }, { title: 'Flatten' }],
}

// Deliberately two agents. No panel, no plan agent, no reviewers, no coordinator.
// The point is to see what the nine missing agents were doing, so nothing here
// compensates for their absence.

const given = typeof args === 'string' ? args : (args && args.folder) || './material/'
const folder = given.replace(/\/+$/, '') + '/'
const slug = (folder.replace(/\/+$/, '').split('/').pop() || 'run').toLowerCase().replace(/[^a-z0-9]+/g, '-')
const passed = (args && args.root) || '.'
const root = (!passed || passed.includes('CLAUDE_PLUGIN_ROOT') ? '.' : passed).replace(/\/+$/, '')
const stamp = String((args && args.stamp) || '').replace(/[^0-9A-Za-z-]/g, '').slice(0, 32)
const out = stamp ? `runs/${slug}/${stamp}` : `runs/${slug}`
const R = `${root}/skills/simply/references`

const brief = (task) => `You are one of only two agents in a stripped-down Simply Strategy run.
Read ${R}/house-rules.md first. It applies to everything you write.
The plugin root is \`${root}\`. Where a reference file writes {root}, that is the value; where it
writes a bare skills/, scripts/, templates/ or design/ path, prefix it with the same root.
The material is in ${folder}. There is no intake file for this run. Output goes to ${out}/.

There is no panel and there are no reviewers in this run. Nothing downstream will catch an invented
figure, a date that is not in the source, or a claim the material does not support. So the rule that
matters most here is the one you cannot lean on anyone else for:

  Every number, date, name and owner you write must appear in the material. If it does not, write
  [TO FILL: what is needed]. Your own arithmetic on their figures is allowed and must be labelled as
  yours. Do not round, do not estimate, do not infer a date from a period.

${task}
Write only the files you are told to write. Return one line: the path you wrote.`

log(`ablation: two agents, no panel, no reviewers. material ${folder}`)

phase('Spec')
await agent(brief(`Your step is "1 · spec" in ${R}/pipeline.md. Follow it and write ${out}/01-spec.md.`),
  { label: 'spec', phase: 'Spec' })

phase('Flatten')
await agent(brief(`Your step is "4 · flatten" in ${R}/pipeline.md, with one difference: there is no
03-plan.md, because no plan agent ran. Work from ${out}/01-spec.md and the material itself.

That means the two things step 3 normally owes you do not exist. You owe them instead: the governing
thought, and the through-line as one claim per section which becomes the headings. Both are defined
in the "Then write the argument" part of step 3 in ${R}/pipeline.md. Read it.

Load ${root}/skills/flatten/SKILL.md and read ${root}/skills/flatten/references/output.md and
before-after.md first. Write ${out}/04-plain.md.`),
  { label: 'flatten', phase: 'Flatten' })

return { slug, folder, out, plain: `${out}/04-plain.md` }
