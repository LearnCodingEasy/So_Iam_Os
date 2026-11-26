<script setup>
// ============================================================
//  RealtimeGraph.vue
//  src/components/Automation/Execution/RealtimeGraph.vue
//
//  المسؤولية: رسم بياني للـ metrics أثناء تنفيذ الـ Workflow
//  يعرض:
//   - عدد الـ nodes المنفّذة vs الكلي
//   - وقت التنفيذ لكل node
//   - success rate
//
//  الاستخدام:
//    <RealtimeGraph
//      :task-run-id="currentTaskRunId"
//      :nodes="nodes"
//      :visible="showGraph"
//      @close="showGraph = false"
//    />
// ============================================================
import { ref, computed, watch, onBeforeUnmount } from 'vue'

const props = defineProps({
  visible: { type: Boolean, default: false },
  taskRunId: { type: String, default: null },
  nodes: { type: Array, default: () => [] }, // الـ nodes من الـ Canvas
  wsBaseUrl: { type: String, default: 'ws://localhost:8000' },
})

const emit = defineEmits(['close', 'update:visible'])
console.log('emit: ', emit)

// ─── State ────────────────────────────────────────────────
const nodeStats = ref(new Map()) // node_id → { label, status, duration_ms }
const startTime = ref(null)
const elapsed = ref(0)
let ws = null
let timer = null

// ─── Computed Metrics ─────────────────────────────────────
const totalNodes = computed(() => props.nodes.length)
const executedCount = computed(
  () => [...nodeStats.value.values()].filter((s) => s.status !== 'idle').length,
)
const successCount = computed(
  () => [...nodeStats.value.values()].filter((s) => s.status === 'success').length,
)
const failedCount = computed(
  () => [...nodeStats.value.values()].filter((s) => s.status === 'failed').length,
)
const successRate = computed(() => {
  const done = successCount.value + failedCount.value
  return done ? Math.round((successCount.value / done) * 100) : 0
})

const progressPercent = computed(() =>
  totalNodes.value ? Math.round((executedCount.value / totalNodes.value) * 100) : 0,
)

const elapsedFormatted = computed(() => {
  const s = Math.floor(elapsed.value / 1000)
  const ms = elapsed.value % 1000
  return `${s}.${String(ms).padStart(3, '0')}s`
})

// ─── Chart Data (bars for node durations) ─────────────────
const barData = computed(() => {
  return props.nodes.map((n) => {
    const stat = nodeStats.value.get(n.id) ?? { status: 'idle', duration_ms: 0 }
    return {
      id: n.id,
      label: n.data?.label ?? n.id.slice(0, 8),
      status: stat.status,
      duration_ms: stat.duration_ms ?? 0,
    }
  })
})

const maxDuration = computed(() => {
  const max = Math.max(...barData.value.map((b) => b.duration_ms), 1)
  return max
})

const barColor = (status) =>
  ({
    idle: '#334155',
    running: '#3b82f6',
    success: '#22c55e',
    failed: '#ef4444',
  })[status] ?? '#334155'

// ─── WebSocket ────────────────────────────────────────────
const connect = () => {
  if (!props.taskRunId) return

  ws = new WebSocket(`${props.wsBaseUrl}/ws/workflow/${props.taskRunId}/`)

  ws.onopen = () => {
    startTime.value = Date.now()
    timer = setInterval(() => {
      elapsed.value = Date.now() - startTime.value
    }, 100)
  }

  ws.onmessage = ({ data }) => {
    try {
      const msg = JSON.parse(data)
      if (msg.type === 'status' && msg.node_id) {
        const existing = nodeStats.value.get(msg.node_id) ?? {}
        if (msg.status === 'running') {
          nodeStats.value.set(msg.node_id, {
            ...existing,
            status: 'running',
            startedAt: Date.now(),
          })
        } else {
          const started = existing.startedAt ?? Date.now()
          const duration_ms = Date.now() - started
          nodeStats.value.set(msg.node_id, { ...existing, status: msg.status, duration_ms })
        }
        nodeStats.value = new Map(nodeStats.value) // force reactivity
      }
      if (msg.type === 'done') {
        clearInterval(timer)
      }
    } catch (_) {
      console.log('_: ', _)
    }
  }

  ws.onclose = () => clearInterval(timer)
}

watch(
  () => props.taskRunId,
  (id) => {
    if (id && props.visible) {
      nodeStats.value = new Map()
      elapsed.value = 0
      connect()
    }
  },
)

watch(
  () => props.visible,
  (v) => {
    if (v && props.taskRunId) connect()
    if (!v) {
      ws?.close()
      clearInterval(timer)
    }
  },
)

onBeforeUnmount(() => {
  ws?.close()
  clearInterval(timer)
})
</script>

<template>
  <div>
    <div class="graph-panel-wrapper">
      <!-- ── Summary Cards ──────────────────────────── -->
      <div class="summary-cards">
        <div class="stat-card">
          <span class="stat-card__value">{{ executedCount }}/{{ totalNodes }}</span>
          <span class="stat-card__label">Nodes Executed</span>
        </div>
        <div class="stat-card stat-card--success">
          <span class="stat-card__value">{{ successCount }}</span>
          <span class="stat-card__label">✅ Success</span>
        </div>
        <div class="stat-card stat-card--error">
          <span class="stat-card__value">{{ failedCount }}</span>
          <span class="stat-card__label">❌ Failed</span>
        </div>
        <div class="stat-card">
          <span class="stat-card__value">{{ successRate }}%</span>
          <span class="stat-card__label">Success Rate</span>
        </div>
        <div class="stat-card">
          <span class="stat-card__value">{{ elapsedFormatted }}</span>
          <span class="stat-card__label">Elapsed</span>
        </div>
      </div>

      <!-- ── Progress Bar ────────────────────────────── -->
      <div class="progress-section">
        <div class="flex justify-between text-xs text-slate-400 mb-1">
          <span>Progress</span>
          <span>{{ progressPercent }}%</span>
        </div>
        <prime_progress_bar :value="progressPercent" :show-value="false" style="height: 6px" />
      </div>

      <!-- ── Bar Chart: Node Durations ──────────────── -->
      <div class="chart-section">
        <h4 class="chart-title">⏱️ Execution Time per Node</h4>

        <div v-if="!barData.length" class="chart-empty">لا يوجد nodes بعد</div>

        <div v-else class="bar-chart">
          <div v-for="bar in barData" :key="bar.id" class="bar-row">
            <!-- Label -->
            <div class="bar-label" :title="bar.label">{{ bar.label }}</div>

            <!-- Bar -->
            <div class="bar-track">
              <div
                class="bar-fill"
                :style="{
                  width: maxDuration ? (bar.duration_ms / maxDuration) * 100 + '%' : '0%',
                  background: barColor(bar.status),
                  minWidth: bar.status !== 'idle' ? '4px' : '0',
                }"
              >
                <span v-if="bar.status === 'running'" class="bar-pulse"></span>
              </div>
            </div>

            <!-- Duration -->
            <div class="bar-value">
              <span v-if="bar.status === 'idle'" class="text-slate-600">—</span>
              <span v-else-if="bar.status === 'running'">
                <i class="pi pi-spin pi-spinner text-blue-400" style="font-size: 0.7rem"></i>
              </span>
              <span v-else>{{ bar.duration_ms }}ms</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <prime_button
      label="إغلاق"
      severity="secondary"
      outlined
      @click="$emit('update:visible', false)"
    />
  </div>
</template>

<style scoped>
/* ── Wrapper ───────────────────────────────── */
.graph-panel-wrapper {
  width: 100%;
  background: #0d1117;
  border-top: 1px solid #334155;
  max-height: 280px; /* ✅ مش بييجي فوق الـ LiveConsole */
  overflow-y: auto;
  padding: 12px 16px;
}

/* ── Header ────────────────────────────────── */
.graph-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  font-size: 0.82rem;
  font-weight: 700;
  color: #94a3b8;
}

/* ── Summary Cards ─────────────────────────── */
.summary-cards {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 12px;
}

.stat-card {
  flex: 1;
  min-width: 80px;
  background: #1e293b;
  border: 1px solid #334155;
  border-radius: 8px;
  padding: 8px 10px; /* ✅ أصغر من الأصل عشان يتلاءم مع الـ strip */
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.stat-card--success {
  border-color: rgba(34, 197, 94, 0.4);
}
.stat-card--error {
  border-color: rgba(239, 68, 68, 0.4);
}
.stat-card__value {
  font-size: 1.1rem;
  font-weight: 700;
  color: #e2e8f0;
}
.stat-card__label {
  font-size: 0.65rem;
  color: #64748b;
}

/* ── Progress ──────────────────────────────── */
.progress-section {
  padding: 0 2px;
  margin-bottom: 12px;
}

/* ── Chart ─────────────────────────────────── */
.chart-section {
  background: #1e293b;
  border: 1px solid #334155;
  border-radius: 8px;
  padding: 12px;
}

.chart-title {
  font-size: 0.78rem;
  font-weight: 600;
  color: #94a3b8;
  margin-bottom: 10px;
}
.chart-empty {
  text-align: center;
  color: #475569;
  font-size: 0.78rem;
  padding: 16px;
}
.bar-chart {
  display: flex;
  flex-direction: column;
  gap: 5px;
}
.bar-row {
  display: flex;
  align-items: center;
  gap: 8px;
}
.bar-label {
  width: 90px;
  font-size: 0.7rem;
  color: #94a3b8;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex-shrink: 0;
  text-align: right;
}
.bar-track {
  flex: 1;
  height: 14px;
  background: #0f172a;
  border-radius: 3px;
  overflow: hidden;
}
.bar-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.3s ease;
  position: relative;
}
.bar-value {
  width: 48px;
  font-size: 0.68rem;
  color: #64748b;
  text-align: right;
  flex-shrink: 0;
}

.bar-pulse {
  position: absolute;
  right: 0;
  top: 0;
  height: 100%;
  width: 20px;
  background: rgba(255, 255, 255, 0.3);
  animation: pulse-bar 1s ease-in-out infinite;
}

@keyframes pulse-bar {
  0%,
  100% {
    opacity: 0.3;
  }
  50% {
    opacity: 0.8;
  }
}
</style>
