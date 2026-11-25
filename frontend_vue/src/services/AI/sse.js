/** Parse an SSE event block without assuming one data line or LF-only endings. */
export function parseSSEEvent(block) {
  let type = 'message'
  const data = []
  for (const rawLine of block.split(/\r?\n/)) {
    if (!rawLine || rawLine.startsWith(':')) continue
    const separator = rawLine.indexOf(':')
    const field = separator < 0 ? rawLine : rawLine.slice(0, separator)
    let value = separator < 0 ? '' : rawLine.slice(separator + 1)
    if (value.startsWith(' ')) value = value.slice(1)
    if (field === 'event') type = value || 'message'
    if (field === 'data') data.push(value)
  }
  if (!data.length) return null
  const raw = data.join('\n')
  let parsed
  try {
    parsed = JSON.parse(raw)
  } catch {
    parsed = { raw }
  }
  if (type === 'message' && parsed && typeof parsed.delta === 'string') type = 'delta'
  return { type, data: parsed }
}

/** Incrementally consume a POST SSE response and flush the final unterminated block. */
export async function consumeSSEStream(stream, onEvent) {
  const reader = stream.getReader()
  const decoder = new TextDecoder()
  let buffer = ''
  const dispatch = (block) => {
    const event = parseSSEEvent(block)
    if (event) onEvent(event)
  }
  try {
    while (true) {
      const { value, done } = await reader.read()
      if (done) break
      buffer += decoder.decode(value, { stream: true })
      let boundary
      while ((boundary = /\r?\n\r?\n/.exec(buffer))) {
        dispatch(buffer.slice(0, boundary.index))
        buffer = buffer.slice(boundary.index + boundary[0].length)
      }
    }
    buffer += decoder.decode()
    if (buffer.trim()) dispatch(buffer)
  } catch (error) {
    try {
      await reader.cancel(error)
    } catch {
      /* reader already closed */
    }
    throw error
  } finally {
    reader.releaseLock?.()
  }
}
