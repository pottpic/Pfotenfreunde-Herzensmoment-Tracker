import { atom, read, update } from 'claude-code'
import type { Register } from 'claude-code'

import type { Limit } from '../types'

const limits = atom({ plugin: 'limit-balken', key: 'limits' } as const, [] as Limit[])

const NAMES: Record<string, string> = { five_hour: '5 Std', seven_day: 'Woche' }
const WIDTH = 12

function color(p: number): string {
  if (p >= 90) return '#d9534f'
  if (p >= 70) return '#e0a030'
  return '#5cb85c'
}

function resetText(iso: string | undefined, now: number): string {
  if (!iso) return ''
  const ms = Date.parse(iso) - now
  if (!Number.isFinite(ms) || ms <= 0) return ''
  const min = Math.round(ms / 60000)
  if (min < 60) return ` · noch ${min} Min`
  const h = Math.floor(min / 60)
  if (h < 48) return ` · noch ${h} Std ${min % 60} Min`
  return ` · noch ${Math.floor(h / 24)} T ${h % 24} Std`
}

export const register: Register = on => {
  const keep = (rl: Limit[]) => rl.filter(l => l.kind in NAMES).map(l => ({ ...l }))

  on('session.start', async ($, e, next) => {
    const r = await next(e)
    const u = await $.session.usage()
    await update($, limits, () => keep(u.rateLimits))
    return r
  })

  on('session.measure', async ($, e, next) => {
    await update($, limits, () => keep(e.rateLimits))
    return next(e)
  })

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    const list = await read($, limits)
    if (e.props.hasSurvey) return next(e)
    const { Box, Text } = $.ui.resolve(e)
    const now = await $.clock.now()

    if (list.length === 0) {
      return (
        <Box>
          <Text dimColor>Limits: noch keine Werte (kommen nach der ersten Antwort)</Text>
        </Box>
      )
    }

    const order = ['five_hour', 'seven_day']
    const sorted = [...list].sort((a, b) => order.indexOf(a.kind) - order.indexOf(b.kind))

    return (
      <Box flexDirection="row" gap={3} flexWrap="wrap">
        {sorted.map(l => {
          const p = Math.max(0, Math.min(100, l.percentUsed))
          const filled = Math.round((p / 100) * WIDTH)
          return (
            <Box key={l.kind} flexDirection="row" gap={1} alignItems="center">
              <Text bold>{NAMES[l.kind]}</Text>
              <Box flexDirection="row" width={WIDTH} height={1} backgroundColor="#444444">
                {filled > 0 ? <Box width={filled} height={1} backgroundColor={color(p)} /> : null}
              </Box>
              <Text tabular>
                {Math.round(p)}%
              </Text>
              <Text dimColor>{resetText(l.resetsAt, now)}</Text>
            </Box>
          )
        })}
      </Box>
    )
  })
}
