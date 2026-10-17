import { beforeEach, describe, expect, it } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useCodexStore } from '@/stores/codex'

describe('Codex capability registry contract', () => {
  beforeEach(() => setActivePinia(createPinia()))
  it('defines the expected registry collections', () => {
    const store = useCodexStore()
    expect(store.capabilityFeatures).toEqual([])
    expect(store.capabilityTools).toEqual([])
    expect(store.capabilityAgents).toEqual([])
  })
})
