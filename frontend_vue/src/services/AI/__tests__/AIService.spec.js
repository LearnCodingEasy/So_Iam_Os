import { describe, expect, it, vi } from 'vitest'
import { ReadableStream } from 'node:stream/web'
import { TextEncoder } from 'node:util'
import { consumeSSEStream, parseSSEEvent } from '../sse'

function streamFrom(parts) {
  const encoder = new TextEncoder()
  let index = 0
  return new ReadableStream({
    pull(controller) {
      if (index >= parts.length) return controller.close()
      controller.enqueue(encoder.encode(parts[index++]))
    },
  })
}

describe('AI POST-SSE parser', () => {
  it('parses meta, delta and done events across chunk boundaries', async () => {
    const events = []
    const stream = streamFrom([
      'event: meta\r\ndata: {"conversation_id":12,"provider":"ollama"}\r\n\r',
      '\nevent: message\ndata: {"delta":"Hello "}\n\n',
      'event: done\ndata: {"message_id":44,"content":"Hello world"}\n\n',
    ])
    await consumeSSEStream(stream, (event) => events.push(event))
    expect(events).toEqual([
      { type: 'meta', data: { conversation_id: 12, provider: 'ollama' } },
      { type: 'delta', data: { delta: 'Hello ' } },
      { type: 'done', data: { message_id: 44, content: 'Hello world' } },
    ])
  })

  it('flushes the last event when the server closes without a blank-line delimiter', async () => {
    const callback = vi.fn()
    await consumeSSEStream(
      streamFrom(['event: error\ndata: {"error":"provider unavailable"}']),
      callback,
    )
    expect(callback).toHaveBeenCalledWith({
      type: 'error',
      data: { error: 'provider unavailable' },
    })
  })

  it('supports multiline data fields and ignores comment heartbeats', () => {
    expect(parseSSEEvent(': heartbeat\nevent: custom\ndata: {"value":\ndata: 7}')).toEqual({
      type: 'custom',
      data: { value: 7 },
    })
  })
})
