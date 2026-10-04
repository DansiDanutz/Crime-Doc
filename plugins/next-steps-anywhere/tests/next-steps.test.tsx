import { expect, test } from 'claude-code/testing'
import type { On, RenderPropsOf, TurnCompleteInput } from 'claude-code'

const PLUGIN = 'next-steps-anywhere'
// AbovePrompt is raised on the terminal and desktop only; mobile and VS Code use the pane.
const BAND_SURFACES = ['terminal', 'desktop'] as const
const PANE_SURFACES = ['mobile', 'vscode', 'terminal', 'desktop'] as const
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
const RUN_NEXT = {
  command: 'next-steps',
  args: '',
  origin: { kind: 'composer' as const },
  presentation: { isFullscreen: false, columns: 80 },
}
const PANE_PROPS: RenderPropsOf['Pane'] = {
  title: 'Next steps',
  isFocused: false,
  bodyColumns: 60,
  placement: 'inline',
  scroll: { offset: 0, bodyRows: 8 },
  view: {},
}

function turn(answer: string, extra: Partial<TurnCompleteInput> = {}): TurnCompleteInput {
  return { reason: 'answer', answer, durationMs: 10, isAborted: false, turnId: 't1', ...extra } as TurnCompleteInput
}

/** The engine beneath the plugin: a forked model that answers `reply`, and records of fills/forks. */
function engine(on: On, reply: string, fail: { fork?: boolean; forkGate?: Promise<void> } = {}) {
  const seen = { forks: 0, fills: [] as string[], suggested: [] as string[], opened: [] as string[], closed: [] as string[] }
  on('turn.complete', () => ({ text: 'engine result' }))
  on('turn.start', ($, e) => ({ turnId: e.turnId }))
  on('command.list', () => ({ value: [{ name: 'code-review', description: 'Review the diff', source: 'user' as const }] }))
  on('ui.render', ($, e) => {
    const { Box } = $.ui.resolve(e)
    return <Box />
  })
  on('model.fork', async () => {
    seen.forks += 1
    if (fail.fork) throw new Error('fork unavailable')
    if (fail.forkGate) await fail.forkGate
    return { value: { isAnswered: true as const, text: reply, usage: USAGE } }
  })
  on('session.start', ($, e) => ({ cwd: e.cwd }))
  on('command.register', ($, e) => ({ value: { command: e.name } }))
  on('ui.open', ($, e) => {
    seen.opened.push(e.id)
    return { value: { isPlaced: true as const } }
  })
  on('ui.close', ($, e) => {
    seen.closed.push(e.id)
    return { value: undefined }
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

test('the band shows on the terminal and desktop, fills the box when pressed, then clears', async ($, on) => {
  const seen = engine(on, '["run the tests", "update the README", "/code-review high"]')
  for (const surface of BAND_SURFACES) {
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
  expect(seen.suggested).toEqual([])
})

test('/next-steps opens the list in a pane on every surface, and a press fills and closes it', async ($, on) => {
  const seen = engine(on, '["run the tests", "update the README"]')
  for (const surface of PANE_SURFACES) {
    await $.turn.complete(turn(LONG_ANSWER))
    await $.command.run(RUN_NEXT)
    expect(seen.opened.at(-1)).toBe('next-steps')

    const pane = await $.ui.mount({ plugin: PLUGIN, surface, component: 'Pane', requestId: 'next-steps', props: PANE_PROPS })
    expect(await pane.find({ key: 'suggestion-2' })).toBeDefined()
    await pane.press({ key: 'suggestion-1' })
    expect(seen.fills.at(-1)).toBe('run the tests')
    expect(seen.closed.at(-1)).toBe('next-steps')
    await pane.unmount()
  }
})

test('/next-steps with nothing to suggest says so and opens no pane', async ($, on) => {
  const seen = engine(on, '[]')
  const ran = await $.command.run(RUN_NEXT)
  expect(ran.text).toContain('No suggestions yet')
  expect(seen.opened).toEqual([])
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

test('a fork that throws shows nothing and does not fail the turn', async ($, on) => {
  engine(on, '["anything"]', { fork: true })
  expect(await $.turn.complete(turn(LONG_ANSWER))).toEqual({ text: 'engine result' })
  const ui = await $.ui.mount({ plugin: PLUGIN, surface: 'terminal', component: 'AbovePrompt', props: BAND })
  expect(await ui.find({ type: 'Button' })).toBeUndefined()
})

test('a reply that lands after the next prompt cleared the band does not bring old suggestions back', async ($, on) => {
  let release = () => {}
  const forkGate = new Promise<void>(resolve => {
    release = resolve
  })
  engine(on, '["stale suggestion"]', { forkGate })
  const completing = $.turn.complete(turn(LONG_ANSWER))
  await $.turn.start({ text: 'next prompt', turnId: 't2' } as Parameters<typeof $.turn.start>[0])
  release()
  await completing

  const ui = await $.ui.mount({ plugin: PLUGIN, surface: 'terminal', component: 'AbovePrompt', props: BAND })
  expect(await ui.find({ key: 'suggestion-1' })).toBeUndefined()
})
