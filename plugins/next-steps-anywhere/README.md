# next-steps-anywhere

After each answer, suggests up to three next prompts. In the terminal and the desktop app they
appear above the input box on their own; on any surface (mobile and VS Code included) type
`/next-steps` to open them in a pane.

```
next:
  1: run the tests you just wrote
  2: do the same for the settings page
  3: /code-review high
  dismiss
```

Tap a suggestion (or press `1`, `2`, `3` from an empty prompt box) and it is written into the box
as a draft — edit it, then send it yourself. `0` / **dismiss** clears them. It never submits a prompt on its own.

## Install (all projects)

```bash
claude plugin marketplace add DansiDanutz/Crime-Doc
claude plugin install next-steps-anywhere@dansidanutz --scope user
```

## How it works

A function-hooks plugin (`hooks/register.tsx`):

- `turn.complete` — after a main-loop answer of at least `minAnswerChars`, asks
  `$.model.fork` for likely next prompts. The fork reuses the session's prompt cache, so it costs
  about one short reply per turn.
- `$.command.list` — the session's skills and slash commands go into the question, so a suggestion
  can be one of them; a suggestion naming a command the session lacks is dropped.
- `ui.render` on `AbovePrompt` — draws the suggestions as buttons above the prompt. Claude Code
  raises that site on the terminal and desktop only.
- `/next-steps` — opens the same buttons in a `Pane`, which every surface (mobile and VS Code
  included) draws.
- A press calls `$.prompt.fill`. The plugin leaves the box's dim ghost text (`$.prompt.suggest`)
  to Claude Code's own suggestion.
- `turn.start` / `prompt.submit` — clear stale suggestions.

Skipped after subagent turns, interrupted turns, errors and short answers.

## Options

| Option | Default | What it does |
| --- | --- | --- |
| `minAnswerChars` | `80` | Skip suggestions after answers shorter than this |
| `suggestSkills` | `true` | Tell the suggester which skills and slash commands the session has |

## Checks

```bash
claude plugin validate plugins/next-steps-anywhere
claude plugin test plugins/next-steps-anywhere
```
