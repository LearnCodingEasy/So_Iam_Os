import test from 'node:test'
import assert from 'node:assert/strict'
import { ReadableStream } from 'node:stream/web'
import { TextEncoder } from 'node:util'
import { consumeSSEStream, parseSSEEvent } from '../src/services/sse.js'

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

test('POST SSE parses meta, delta and done events across chunk boundaries', async () => {
  const events = []
  await consumeSSEStream(streamFrom([
    'event: meta\r\ndata: {"conversation_id":12,"provider":"ollama"}\r\n\r',
    '\nevent: message\ndata: {"delta":"Hello "}\n\n',
    'event: done\ndata: {"message_id":44,"content":"Hello world"}\n\n',
  ]), (event) => events.push(event))
  assert.deepEqual(events, [
    { type: 'meta', data: { conversation_id: 12, provider: 'ollama' } },
    { type: 'delta', data: { delta: 'Hello ' } },
    { type: 'done', data: { message_id: 44, content: 'Hello world' } },
  ])
})

test('POST SSE flushes a final event without a terminating blank line', async () => {
  const events = []
  await consumeSSEStream(streamFrom(['event: error\ndata: {"error":"provider unavailable"}']), (event) => events.push(event))
  assert.deepEqual(events, [{ type: 'error', data: { error: 'provider unavailable' } }])
})

test('SSE parser joins multiline data and ignores heartbeat comments', () => {
  assert.deepEqual(parseSSEEvent(': heartbeat\nevent: custom\ndata: {"value":\ndata: 7}'), {
    type: 'custom', data: { value: 7 },
  })
})
