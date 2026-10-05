export type Suggestions = { turnId: string; items: string[] }

declare module 'claude-code' {
  interface PluginState {
    'next-steps-anywhere': { suggestions: Suggestions | null }
  }
}
