<template>
  <div class="afp-wrap" :class="{ 'afp-compact': compact }">
    <!-- Header -->
    <div class="afp-header" v-if="!compact">
      <div class="afp-header-left">
        <div class="afp-logo">⚡</div>
        <div>
          <div class="afp-title">API Flow Tracker</div>
          <div class="afp-sub" v-if="meta?.url">
            <span class="afp-method" :class="`m-${(meta.method || 'GET').toLowerCase()}`">{{
              meta.method
            }}</span>
            <span class="afp-url">{{ meta.url }}</span>
          </div>
        </div>
      </div>
      <div class="afp-header-right">
        <div class="afp-timing" v-if="meta?.duration">{{ meta.duration }}ms</div>
        <div class="afp-status-badge" :class="overallClass">{{ overallLabel }}</div>
      </div>
    </div>

    <!-- Pipeline -->
    <div class="afp-pipeline">
      <template v-for="(stage, i) in stages" :key="stage.id">
        <!-- Stage node -->
        <div
          class="afp-node"
          :class="[`s-${stage.status}`, { 'afp-node--active': stage.status === 'active' }]"
          @click="toggleDetail(i)"
        >
          <div class="afp-node-ring">
            <div class="afp-node-inner">
              <span v-if="stage.status === 'active'" class="afp-spinner"></span>
              <span v-else-if="stage.status === 'pass'">✓</span>
              <span v-else-if="stage.status === 'fail'">✗</span>
              <span v-else-if="stage.status === 'skip'">–</span>
              <span v-else>{{ stage.icon }}</span>
            </div>
          </div>
          <div class="afp-node-label">{{ stage.label }}</div>
          <div class="afp-node-layer">{{ stage.layer }}</div>
          <div class="afp-node-timing" v-if="stage.timing && typeof stage.timing === 'number'">
            {{ stage.timing }}ms
          </div>
        </div>

        <!-- Connector (not after last) -->
        <div v-if="i < stages.length - 1" class="afp-connector" :class="getConnectorClass(i)">
          <div class="afp-connector-line"></div>
          <div class="afp-connector-arrow">›</div>
        </div>
      </template>
    </div>

    <!-- Detail panel (click on node to expand) -->
    <transition name="afp-slide">
      <div class="afp-detail" v-if="openIdx !== null && stages[openIdx]?.detail">
        <div class="afp-detail-header">
          <span>{{ stages[openIdx].icon }} {{ stages[openIdx].label }}</span>
          <span class="afp-detail-badge" :class="`b-${stages[openIdx].status}`">
            {{ stages[openIdx].status }}
          </span>
        </div>
        <div class="afp-detail-body">{{ stages[openIdx].detail }}</div>
      </div>
    </transition>

    <!-- Request / Response panels -->
    <div class="afp-data-row" v-if="showData && (meta?.requestBody || meta?.responseBody)">
      <div class="afp-data-panel" v-if="meta?.requestBody">
        <div class="afp-data-label">📤 ما اتبعت</div>
        <pre class="afp-data-code">{{ meta.requestBody }}</pre>
      </div>

      <div
        class="afp-data-panel"
        :class="error ? 'afp-data-panel--error' : 'afp-data-panel--ok'"
        v-if="meta?.responseBody"
      >
        <div class="afp-data-label">
          📥 ما رجع
          <span class="afp-status-chip" :class="statusChipClass">{{ meta.status }}</span>
        </div>
        <pre class="afp-data-code">{{ meta.responseBody }}</pre>
      </div>
    </div>

    <!-- Error explainer -->
    <transition name="afp-slide">
      <div class="afp-error-box" v-if="error?.detail">
        <div class="afp-error-title">🚨 {{ error.detail.short }}</div>
        <div class="afp-error-fix">💡 {{ error.detail.fix }}</div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  stages: { type: Array, default: () => [] },
  meta: { type: Object, default: null },
  error: { type: Object, default: null },
  compact: { type: Boolean, default: false },
  showData: { type: Boolean, default: true },
})

const openIdx = ref(null)

function toggleDetail(i) {
  openIdx.value = openIdx.value === i ? null : i
}

function getConnectorClass(i) {
  const cur = props.stages[i]?.status
  // eslint-disable-next-line no-unused-vars
  const next = props.stages[i + 1]?.status
  if (cur === 'fail') return 'conn-fail'
  if (cur === 'pass') return 'conn-pass'
  if (cur === 'active') return 'conn-active'
  return 'conn-idle'
}

const overallClass = computed(() => {
  const hasFail = props.stages.some((s) => s.status === 'fail')
  const hasActive = props.stages.some((s) => s.status === 'active')
  const allDone = props.stages.find((s) => s.id === 'done')?.status === 'pass'
  if (hasActive) return 'ob-loading'
  if (hasFail) return 'ob-error'
  if (allDone) return 'ob-success'
  return 'ob-idle'
})

const overallLabel = computed(() => {
  const hasFail = props.stages.some((s) => s.status === 'fail')
  const hasActive = props.stages.some((s) => s.status === 'active')
  const allDone = props.stages.find((s) => s.id === 'done')?.status === 'pass'
  if (hasActive) return 'جاري…'
  if (hasFail) return 'فشل'
  if (allDone) return 'نجح ✓'
  return 'في الانتظار'
})

const statusChipClass = computed(() => {
  const s = props.meta?.status
  if (!s) return ''
  if (s < 300) return 'chip-ok'
  if (s < 400) return 'chip-info'
  if (s < 500) return 'chip-warn'
  return 'chip-err'
})
</script>

<style scoped>
/* ── Variables ── */
.afp-wrap {
  --afp-bg: #0d1018;
  --afp-s1: #131720;
  --afp-s2: #1a2030;
  --afp-bd: #232b3e;
  --afp-bd2: #2e3a52;
  --afp-tx: #c8d4f0;
  --afp-mu: #4e5e80;
  --afp-ok: #4ade80;
  --afp-er: #ff6b6b;
  --afp-wa: #fbbf24;
  --afp-in: #38bdf8;
  --afp-acc: #5b8af5;
  --afp-vue: #42d392;
  --afp-dj: #44b78b;
  --afp-net: #a78bfa;

  background: var(--afp-bg);
  border: 1px solid var(--afp-bd);
  border-radius: 14px;
  padding: 16px;
  font-family: 'Tajawal', 'Cairo', sans-serif;
  color: var(--afp-tx);
  direction: rtl;
  width: 100%;
  border-radius: 0;
  border-left: none;
  border-right: none;
  border-bottom: none;
}

/* ── Header ── */
.afp-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--afp-bd);
}
.afp-header-left {
  display: flex;
  align-items: center;
  gap: 10px;
}
.afp-logo {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: linear-gradient(135deg, var(--afp-acc), #8b5cf6);
  display: grid;
  place-items: center;
  font-size: 15px;
  flex-shrink: 0;
}
.afp-title {
  font-size: 14px;
  font-weight: 800;
}
.afp-sub {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 2px;
}
.afp-method {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  font-weight: 700;
  padding: 1px 6px;
  border-radius: 3px;
}
.m-get {
  background: rgba(56, 189, 248, 0.15);
  color: var(--afp-in);
}
.m-post {
  background: rgba(91, 138, 245, 0.15);
  color: var(--afp-acc);
}
.m-put {
  background: rgba(251, 191, 36, 0.15);
  color: var(--afp-wa);
}
.m-patch {
  background: rgba(167, 139, 250, 0.15);
  color: var(--afp-net);
}
.m-delete {
  background: rgba(255, 107, 107, 0.15);
  color: var(--afp-er);
}
.afp-url {
  font-size: 11px;
  color: var(--afp-mu);
  font-family: 'JetBrains Mono', monospace;
}
.afp-header-right {
  display: flex;
  align-items: center;
  gap: 8px;
}
.afp-timing {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  color: var(--afp-mu);
}
.afp-status-badge {
  font-size: 12px;
  font-weight: 700;
  padding: 3px 10px;
  border-radius: 100px;
}
.ob-idle {
  background: rgba(78, 90, 120, 0.2);
  color: var(--afp-mu);
}
.ob-loading {
  background: rgba(91, 138, 245, 0.15);
  color: var(--afp-acc);
}
.ob-success {
  background: rgba(74, 222, 128, 0.12);
  color: var(--afp-ok);
}
.ob-error {
  background: rgba(255, 107, 107, 0.12);
  color: var(--afp-er);
}

/* ── Pipeline ── */
.afp-pipeline {
  display: flex;
  align-items: center;
  gap: 0;
  overflow-x: auto;
  padding: 8px 0 12px;
  scrollbar-width: thin;
  scrollbar-color: var(--afp-bd2) transparent;
}

/* ── Node ── */
.afp-node {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  flex-shrink: 0;
  padding: 6px 8px;
  border-radius: 8px;
  transition: background 0.15s;
  min-width: 72px;
}
.afp-node:hover {
  background: rgba(255, 255, 255, 0.04);
}

.afp-node-ring {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  border: 2px solid var(--afp-bd2);
  display: grid;
  place-items: center;
  transition: all 0.3s;
  position: relative;
}
.afp-node-inner {
  font-size: 16px;
  font-weight: 700;
}

/* Status colors */
.s-idle .afp-node-ring {
  border-color: var(--afp-bd2);
  opacity: 0.5;
}
.s-active .afp-node-ring {
  border-color: var(--afp-acc);
  box-shadow: 0 0 0 4px rgba(91, 138, 245, 0.2);
  animation: ring-pulse 1s ease infinite;
}
@keyframes ring-pulse {
  0%,
  100% {
    box-shadow: 0 0 0 3px rgba(91, 138, 245, 0.25);
  }
  50% {
    box-shadow: 0 0 0 7px rgba(91, 138, 245, 0.08);
  }
}
.s-pass .afp-node-ring {
  border-color: var(--afp-ok);
  background: rgba(74, 222, 128, 0.08);
}
.s-fail .afp-node-ring {
  border-color: var(--afp-er);
  background: rgba(255, 107, 107, 0.1);
}
.s-warn .afp-node-ring {
  border-color: var(--afp-wa);
  background: rgba(251, 191, 36, 0.08);
}
.s-skip .afp-node-ring {
  border-color: var(--afp-bd2);
  opacity: 0.4;
}

.s-pass .afp-node-inner {
  color: var(--afp-ok);
  font-size: 18px;
}
.s-fail .afp-node-inner {
  color: var(--afp-er);
  font-size: 18px;
}
.s-skip .afp-node-inner {
  color: var(--afp-mu);
}
.s-active .afp-node-inner {
  color: var(--afp-acc);
}

.afp-spinner {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  border: 2px solid rgba(91, 138, 245, 0.3);
  border-top-color: var(--afp-acc);
  animation: spin 0.7s linear infinite;
  display: inline-block;
}
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.afp-node-label {
  font-size: 11px;
  font-weight: 700;
  text-align: center;
  color: var(--afp-tx);
  white-space: nowrap;
}
.s-idle .afp-node-label {
  color: var(--afp-mu);
}

.afp-node-layer {
  font-size: 9px;
  font-family: 'JetBrains Mono', monospace;
  color: var(--afp-mu);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.afp-node-timing {
  font-size: 9px;
  font-family: 'JetBrains Mono', monospace;
  color: var(--afp-mu);
}

/* ── Connector ── */
.afp-connector {
  display: flex;
  align-items: center;
  flex-direction: column;
  padding: 0 2px;
  flex-shrink: 0;
  gap: 2px;
  opacity: 0.5;
  transition: opacity 0.3s;
}
.conn-pass {
  opacity: 1;
}
.conn-active {
  opacity: 1;
}
.conn-fail {
  opacity: 0.3;
}

.afp-connector-line {
  width: 24px;
  height: 2px;
  border-radius: 1px;
  background: var(--afp-bd2);
  transition: background 0.3s;
}
.conn-pass .afp-connector-line {
  background: var(--afp-ok);
}
.conn-active .afp-connector-line {
  background: var(--afp-acc);
  animation: flow-anim 1s linear infinite;
}
.conn-fail .afp-connector-line {
  background: var(--afp-bd2);
}

@keyframes flow-anim {
  0% {
    background: var(--afp-acc);
  }
  50% {
    background: rgba(91, 138, 245, 0.3);
  }
  100% {
    background: var(--afp-acc);
  }
}

.afp-connector-arrow {
  font-size: 12px;
  color: var(--afp-mu);
  line-height: 1;
}
.conn-pass .afp-connector-arrow {
  color: var(--afp-ok);
}
.conn-active .afp-connector-arrow {
  color: var(--afp-acc);
}

/* ── Detail popup ── */
.afp-detail {
  background: var(--afp-s2);
  border: 1px solid var(--afp-bd2);
  border-radius: 8px;
  padding: 10px 14px;
  margin-top: 8px;
}
.afp-detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  font-weight: 700;
  margin-bottom: 6px;
}
.afp-detail-badge {
  font-size: 10px;
  padding: 1px 7px;
  border-radius: 4px;
  font-family: 'JetBrains Mono', monospace;
}
.b-pass {
  background: rgba(74, 222, 128, 0.1);
  color: var(--afp-ok);
}
.b-fail {
  background: rgba(255, 107, 107, 0.1);
  color: var(--afp-er);
}
.b-warn {
  background: rgba(251, 191, 36, 0.1);
  color: var(--afp-wa);
}
.b-skip {
  background: rgba(78, 90, 120, 0.15);
  color: var(--afp-mu);
}
.b-active {
  background: rgba(91, 138, 245, 0.1);
  color: var(--afp-acc);
}
.b-info {
  background: rgba(56, 189, 248, 0.1);
  color: var(--afp-in);
}

.afp-detail-body {
  font-size: 11.5px;
  color: var(--afp-tx);
  line-height: 1.8;
  font-family: 'JetBrains Mono', monospace;
  white-space: pre-wrap;
}

/* ── Data row ── */
.afp-data-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin-top: 10px;
}
@media (max-width: 600px) {
  .afp-data-row {
    grid-template-columns: 1fr;
  }
}

.afp-data-panel {
  background: var(--afp-s2);
  border: 1px solid var(--afp-bd);
  border-radius: 8px;
  overflow: hidden;
}
.afp-data-panel--ok {
  border-color: rgba(74, 222, 128, 0.2);
}
.afp-data-panel--error {
  border-color: rgba(255, 107, 107, 0.2);
}

.afp-data-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  font-weight: 700;
  padding: 7px 10px;
  background: rgba(255, 255, 255, 0.03);
  border-bottom: 1px solid var(--afp-bd);
}
.afp-data-code {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10.5px;
  color: #8ba0c8;
  padding: 8px 10px;
  margin: 0;
  max-height: 130px;
  overflow-y: auto;
  white-space: pre-wrap;
  word-break: break-all;
  scrollbar-width: thin;
  scrollbar-color: var(--afp-bd2) transparent;
}
.afp-status-chip {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  font-weight: 700;
  padding: 1px 6px;
  border-radius: 3px;
}
.chip-ok {
  background: rgba(74, 222, 128, 0.12);
  color: var(--afp-ok);
}
.chip-info {
  background: rgba(56, 189, 248, 0.12);
  color: var(--afp-in);
}
.chip-warn {
  background: rgba(251, 191, 36, 0.12);
  color: var(--afp-wa);
}
.chip-err {
  background: rgba(255, 107, 107, 0.12);
  color: var(--afp-er);
}

/* ── Error box ── */
.afp-error-box {
  background: rgba(255, 107, 107, 0.07);
  border: 1px solid rgba(255, 107, 107, 0.2);
  border-radius: 8px;
  padding: 12px 14px;
  margin-top: 10px;
}
.afp-error-title {
  font-size: 13px;
  font-weight: 800;
  color: var(--afp-er);
  margin-bottom: 6px;
}
.afp-error-fix {
  font-size: 12px;
  color: var(--afp-tx);
  line-height: 1.85;
  white-space: pre-wrap;
}

/* ── Transition ── */
.afp-slide-enter-active,
.afp-slide-leave-active {
  transition: all 0.25s ease;
}
.afp-slide-enter-from,
.afp-slide-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}

/* ── Compact mode ── */
.afp-compact .afp-pipeline {
  padding: 4px 0;
}
.afp-compact .afp-node-ring {
  width: 32px;
  height: 32px;
}
.afp-compact .afp-node-inner {
  font-size: 13px;
}
.afp-compact .afp-node-label {
  font-size: 10px;
}
</style>
