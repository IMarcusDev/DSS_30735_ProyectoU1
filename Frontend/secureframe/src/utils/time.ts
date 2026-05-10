function toUtcDate(iso: string): Date {
  if (iso.endsWith('Z') || iso.includes('+') || iso.includes('-', 10)) return new Date(iso)
  return new Date(iso + 'Z')
}

export function timeAgo(iso: string): string {
  const diffMs = Date.now() - toUtcDate(iso).getTime()
  const diffH  = Math.floor(Math.max(0, diffMs) / 3_600_000)
  if (diffMs < 60_000)   return 'hace un momento'
  if (diffMs < 3_600_000) return `hace ${Math.floor(diffMs / 60_000)}min`
  if (diffH  < 24)        return `hace ${diffH}h`
  const days = Math.floor(diffH / 24)
  return `hace ${days}d`
}

export function hoursAgo(iso: string): number {
  return Math.max(0, (Date.now() - toUtcDate(iso).getTime()) / 3_600_000)
}
