import { expect, test } from 'claude-code/testing'
import type { On, RenderPropsOf, TurnCompleteInput } from 'claude-code'

const PLUGIN = 'next-steps-anywhere'
const SURFACES = ['terminal', 'desktop', 'vscode', 'mobile'] as const
const LONG_ANSWER = 'Done. '.repeat(30)
const USAGE = { input_tokens: 1, output_tokens: 1, cache_read_input_tokens: 0, cache_creation_input_tokens: 0 }
const BAND: RenderPropsOf['AbovePrompt'] = {
  hasSurvey: false,
  isWorking: false,
  maxRows: 8,
  bodyColumns: 100,
  scroll: { offset: 0, bodyRows: 8 },
  view: {},
}

function turn(answer: string, extra: Partial<TurnCompleteInput> = {}): TurnCompleteInput {
  return { reason: 'answer', answer, durationMs: 10, isAborted: false, turnId: 't1', ...extra } as TurnCompleteInput
}

/** The engine beneath the plugin: a forked model that answers `reply`, and records of fills/forks. */
function engine(on: On, reply: string) {
  const seen = { forks: 0, fills: [] as string[], suggested: [] as string[] }
  on('turn.complete', () => ({ text: '' }))
  on('turn.start', ($, e) => ({ turnId: e.turnId }))
  on('command.list', () => ({ value: [{ name: 'code-review', description: 'Review the diff', source: 'user' as const }] }))
  on('ui.render', ($, e) => {
    const { Box } = $.ui.resolve(e)
    return <Box />
  })
  on('model.fork', () => {
    seen.forks += 1
    return { value: { isAnswered: true as const, text: reply, usage: USAGE } }
  })
  on('prompt.fill', ($, e) => {
    seen.fills.push(e.text)
    return { isFilled: true }
  })
  on('prompt.suggest', ($, e) => {
    seen.suggested.push(e.text)
    return { isShown: true }
  })
  return seen
}

test('suggestions show on every surface, fill the box when pressed, then clear', async ($, on) => {
  const seen = engine(on, '["run the tests", "update the README", "/code-review high"]')
  for (const surface of SURFACES) {
    await $.turn.complete(turn(LONG_ANSWER))
    const ui = await $.ui.mount({ plugin: PLUGIN, surface, component: 'AbovePrompt', props: BAND })
    expect(await ui.find({ key: 'suggestion-1' })).toBeDefined()
    expect(await ui.find({ key: 'suggestion-3' })).toBeDefined()
    expect(await ui.find({ key: 'dismiss' })).toBeDefined()

    await ui.press({ key: 'suggestion-2' })
    expect(seen.fills.at(-1)).toBe('update the README')
    expect(await ui.find({ key: 'suggestion-1' })).toBeUndefined()
    await ui.unmount()
  }
  expect(seen.suggested.at(-1)).toBe('run the tests')
})

test('a slash command the session lacks is dropped', async ($, on) => {
  engine(on, '["/deploy prod", "/code-review", "fix the lint errors"]')
  await $.turn.complete(turn(LONG_ANSWER))
  const ui = await $.ui.mount({ plugin: PLUGIN, surface: 'terminal', component: 'AbovePrompt', props: BAND })
  const labels = (await ui.findAll({ type: 'Button' })).map(b => b.props.label)
  expect(labels).toEqual(['/code-review', 'fix the lint errors', 'dismiss'])
})

test('no suggestion is asked for after a short answer, an abort or a subagent turn', async ($, on) => {
  const seen = engine(on, '["anything"]')
  await $.turn.complete(turn('ok'))
  await $.turn.complete(turn(LONG_ANSWER, { reason: 'aborted', isAborted: true }))
  await $.turn.complete(turn(LONG_ANSWER, { agentId: 'sub-1' }))
  expect(seen.forks).toBe(0)
})

test('dismiss clears the band, and a new turn clears stale suggestions', async ($, on) => {
  engine(on, '["one", "two"]')
  await $.turn.complete(turn(LONG_ANSWER))
  const phone = await $.ui.mount({ plugin: PLUGIN, surface: 'mobile', component: 'AbovePrompt', props: BAND })
  await phone.press({ key: 'dismiss' })
  expect(await phone.find({ key: 'suggestion-1' })).toBeUndefined()
  await phone.unmount()

  await $.turn.complete(turn(LONG_ANSWER, { turnId: 't2' }))
  await $.turn.start({ text: 'next prompt', turnId: 't3' } as Parameters<typeof $.turn.start>[0])
  const desk = await $.ui.mount({ plugin: PLUGIN, surface: 'desktop', component: 'AbovePrompt', props: BAND })
  expect(await desk.find({ key: 'suggestion-1' })).toBeUndefined()
})

test('a reply that is not a JSON list shows nothing', async ($, on) => {
  engine(on, 'Sure! You could run the tests next.')
  await $.turn.complete(turn(LONG_ANSWER))
  const ui = await $.ui.mount({ plugin: PLUGIN, surface: 'terminal', component: 'AbovePrompt', props: BAND })
  expect(await ui.find({ type: 'Button' })).toBeUndefined()
})
