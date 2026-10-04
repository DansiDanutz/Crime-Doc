import { atom, read, update } from 'claude-code'
import type { EngineInterface, Register, RenderInput } from 'claude-code'

import type { Suggestions } from '../types'

const suggestions = atom({ plugin: 'next-steps-anywhere', key: 'suggestions' } as const, null as Suggestions | null)

const PANE = 'next-steps'
const COMMAND = 'next-steps'
const MAX_SUGGESTIONS = 3
const MAX_LENGTH = 160
const MAX_COMMANDS = 40

function buildQuestion(commands: { name: string; description: string }[]): string {
  const lines = [
    'Based on this conversation so far, what are the 1 to 3 prompts the user is most likely to send next?',
    'Write each one as the user would type it: short, concrete, in their voice, under 80 characters.',
    'Prefer the obvious next step in the work that is under way; never repeat something already done.',
  ]
  if (commands.length > 0) {
    lines.push(
      'A suggestion may be one of these slash commands (write it as "/name arguments"); never invent others:',
      ...commands.slice(0, MAX_COMMANDS).map(c => `/${c.name} — ${c.description}`),
    )
  }
  lines.push('Reply with ONLY a JSON array of strings and nothing else. If there is no sensible next step, reply [].')
  return lines.join('\n')
}

function parseSuggestions(text: string, known: Set<string> | null): string[] {
  const start = text.indexOf('[')
  const end = text.lastIndexOf(']')
  if (start === -1 || end <= start) return []
  let parsed: unknown
  try {
    parsed = JSON.parse(text.slice(start, end + 1))
  } catch {
    return []
  }
  if (!Array.isArray(parsed)) return []
  const out: string[] = []
  for (const item of parsed) {
    if (typeof item !== 'string') continue
    const s = item.replace(/\s+/g, ' ').trim()
    if (s.length === 0 || s.length > MAX_LENGTH) continue
    if (s.startsWith('/')) {
      const name = s.slice(1).split(' ')[0] ?? ''
      if (known === null || !known.has(name)) continue
    }
    if (!out.includes(s)) out.push(s)
    if (out.length === MAX_SUGGESTIONS) break
  }
  return out
}

async function clear($: EngineInterface): Promise<void> {
  await update($, suggestions, () => null)
  await $.ui.close({ id: PANE })
}

async function suggestNext($: EngineInterface, turnId: string, suggestSkills: boolean): Promise<void> {
  const commands = suggestSkills ? await $.command.list() : []
  const known = suggestSkills ? new Set(commands.map(c => c.name)) : null
  const reply = await $.model.fork({ prompt: buildQuestion(commands) })
  if (!reply.isAnswered) return

  const items = parseSuggestions(reply.text, known)
  if (items.length === 0) return

  // No $.prompt.suggest ghost text: the engine already proposes its own there, and a plugin's
  // proposal can stay pending into a later turn with no way to withdraw it.
  await update($, suggestions, () => ({ turnId, items }))
}

/** The suggestions as buttons: a press writes one into the prompt box as a draft. */
function drawSuggestions(
  $: EngineInterface,
  e: RenderInput<'AbovePrompt' | 'Pane'>,
  items: string[],
  columns: number,
) {
  const { Box, Text, Button } = $.ui.resolve(e)
  return (
    <Box flexDirection="column">
      <Text dimColor>next:</Text>
      {items.map((item, i) => (
        <Button
          key={`suggestion-${i + 1}`}
          hotkey={String(i + 1)}
          plain
          label={fit(item, columns)}
          onPress={async () => {
            await $.prompt.fill({ text: item })
            await clear($)
          }}
        />
      ))}
      <Button key="dismiss" hotkey="0" plain dimColor label="dismiss" onPress={() => clear($)} />
    </Box>
  )
}

function fit(label: string, columns: number): string {
  const room = Math.max(12, columns - 6)
  return label.length <= room ? label : `${label.slice(0, room - 1)}…`
}

export const register: Register = (on, options) => {
  const minAnswerChars = typeof options.minAnswerChars === 'number' ? options.minAnswerChars : 80
  const suggestSkills = options.suggestSkills !== false

  on('turn.start', async ($, e, next) => {
    await clear($)
    return next(e)
  })

  on('prompt.submit', async ($, e, next) => {
    await clear($)
    return next(e)
  })

  on('turn.complete', async ($, e, next) => {
    const result = await next(e)
    if (e.agentId || e.reason !== 'answer' || e.isAborted || e.answer.trim().length < minAnswerChars) {
      return result
    }

    // Suggestions are optional: a failure here must never fail the turn that already answered.
    try {
      await suggestNext($, e.turnId, suggestSkills)
    } catch {
      // nothing to show this turn
    }
    return result
  })

  // The band above the prompt: raised on the terminal and the desktop app.
  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    const current = await read($, suggestions)
    if (current === null || current.items.length === 0 || e.props.hasSurvey || e.props.isWorking) {
      return next(e)
    }
    return drawSuggestions($, e, current.items, e.props.bodyColumns)
  })

  // Mobile and VS Code raise no AbovePrompt; /next-steps opens the same list in a pane,
  // which every surface draws.
  on('session.start', async ($, e, next) => {
    await $.command.register({ name: COMMAND, description: 'Show suggested next prompts in a pane' })
    return next(e)
  })

  on('command.run', { command: COMMAND }, async $ => {
    const current = await read($, suggestions)
    if (current === null || current.items.length === 0) {
      return { text: 'No suggestions yet: they appear after the next answer.' }
    }
    await $.ui.open({ id: PANE, title: 'Next steps' })
    return {}
  })

  on('ui.render', { component: 'Pane', requestId: PANE }, async ($, e) => {
    const { Text } = $.ui.resolve(e)
    const current = await read($, suggestions)
    if (current === null || current.items.length === 0) return <Text dimColor>No suggestions.</Text>
    return drawSuggestions($, e, current.items, e.viewport?.columns ?? 80)
  })
}
