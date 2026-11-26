<script setup>
/*
===================================================
LiveConsole.vue
src/components/Automation/Execution/LiveConsole.vue

المسؤولية: عرض logs تنفيذ الـ Workflow في real-time
الـ WebSocket: ws://localhost:8000/ws/workflow/{taskRunId}/

الاستخدام:
  <LiveConsole
    v-if="currentTaskRunId"
    :task-run-id="currentTaskRunId"
    @close="currentTaskRunId = null"
  />

الـ Message Format من الـ Django:
  { type: 'log', level: 'info'|'error'|'success', message: '...', node_id: '...' }
  { type: 'status', status: 'running'|'success'|'failed', node_id: '...' }
  { type: 'done', status: 'success'|'failed' }
===================================================
*/
import { ref, watch, onMounted, onBeforeUnmount, nextTick } from 'vue'

const props = defineProps({
  taskRunId: { type: String, required: true },
  wsBaseUrl: { type: String, default: 'ws://localhost:8000' },
  maxLines: { type: Number, default: 500 },
  autoScroll: { type: Boolean, default: true },
  visible: { type: Boolean, default: true },
})

const emit = defineEmits(['close', 'done', 'error'])

// ─── State ────────────────────────────────────────────────
const logs = ref([])
const status = ref('connecting') // connecting | running | success | failed | closed
const ws = ref(null)
const consoleEl = ref(null)
const isMinimized = ref(false)
let pingInterval = null

// ─── WebSocket Setup ──────────────────────────────────────
const connect = () => {
  if (!props.taskRunId) return

  const url = `${props.wsBaseUrl}/ws/workflow/${props.taskRunId}/`
  ws.value = new WebSocket(url)

  ws.value.onopen = () => {
    status.value = 'running'
    addLog('info', '🔌 Connected — جاري تنفيذ الـ Workflow...')
    // ping every 30s to keep connection alive
    pingInterval = setInterval(() => {
      if (ws.value?.readyState === WebSocket.OPEN) {
        ws.value.send(JSON.stringify({ type: 'ping' }))
      }
    }, 30000)
  }

  ws.value.onmessage = ({ data }) => {
    try {
      const msg = JSON.parse(data)
      handleMessage(msg)
    } catch {
      addLog('info', data)
    }
  }

  ws.value.onerror = () => {
    status.value = 'failed'
    addLog('error', '❌ WebSocket error — تأكد إن الـ Django Channels شغال')
    emit('error')
  }

  ws.value.onclose = () => {
    status.value = status.value === 'running' ? 'closed' : status.value
    addLog('info', '🔌 Connection closed')
    clearInterval(pingInterval)
  }
}

const handleMessage = (msg) => {
  switch (msg.type) {
    case 'log':
      addLog(msg.level ?? 'info', msg.message, msg.node_id)
      break
    case 'status':
      addLog('info', `Node ${msg.node_id}: ${msg.status}`, msg.node_id)
      break
    case 'done':
      status.value = msg.status ?? 'success'
      addLog(
        msg.status === 'success' ? 'success' : 'error',
        msg.status === 'success'
          ? '✅ Workflow اكتمل بنجاح!'
          : `❌ Workflow فشل: ${msg.error ?? 'unknown error'}`,
      )
      emit('done', msg)
      clearInterval(pingInterval)
      break
    default:
      addLog('info', JSON.stringify(msg))
  }
}

// ─── Add Log Line ──────────────────────────────────────────
const addLog = (level, message, nodeId = null) => {
  logs.value.push({
    id: Date.now() + Math.random(),
    level, // info | error | success | warn
    message,
    nodeId,
    time: new Date().toLocaleTimeString('ar-EG', { hour12: false }),
  })

  // Limit lines
  if (logs.value.length > props.maxLines) {
    logs.value = logs.value.slice(-props.maxLines)
  }

  // Auto scroll
  if (props.autoScroll) {
    nextTick(() => {
      if (consoleEl.value) {
        consoleEl.value.scrollTop = consoleEl.value.scrollHeight
      }
    })
  }
}

// ─── Close ────────────────────────────────────────────────
const closeConsole = () => {
  ws.value?.close()
  clearInterval(pingInterval)
  emit('close')
}

const clearLogs = () => {
  logs.value = []
}

// ─── Level Colors ─────────────────────────────────────────
const levelClass = (level) =>
  ({
    info: 'log-info',
    error: 'log-error',
    success: 'log-success',
    warn: 'log-warn',
  })[level] ?? 'log-info'

// ─── Status Badge ─────────────────────────────────────────
const statusLabel = {
  connecting: '🔄 Connecting...',
  running: '▶️ Running',
  success: '✅ Done',
  failed: '❌ Failed',
  closed: '⏹ Closed',
}

// ─── Lifecycle ────────────────────────────────────────────
onMounted(() => connect())

onBeforeUnmount(() => {
  ws.value?.close()
  clearInterval(pingInterval)
})

watch(
  () => props.taskRunId,
  (newId) => {
    if (newId) {
      ws.value?.close()
      logs.value = []
      status.value = 'connecting'
      connect()
    }
  },
)
</script>

<template>
  <div class="live-console" :class="{ 'live-console--minimized': isMinimized }" v-if="visible">
    <!-- ── Header ───────────────────────────────────── -->
    <div class="console-header">
      <div class="console-header__left">
        <span class="console-title"> <i class="pi pi-terminal mr-2"></i>Live Console </span>
        <Tag
          :value="statusLabel[status]"
          :severity="
            status === 'success'
              ? 'success'
              : status === 'failed'
                ? 'danger'
                : status === 'running'
                  ? 'info'
                  : 'secondary'
          "
          class="!text-xs"
        />
      </div>

      <div class="console-header__right">
        <Button
          icon="pi pi-trash"
          size="small"
          text
          rounded
          @click="clearLogs"
          v-tooltip.top="'مسح الـ logs'"
        />
        <Button
          :icon="isMinimized ? 'pi pi-chevron-up' : 'pi pi-chevron-down'"
          size="small"
          text
          rounded
          @click="isMinimized = !isMinimized"
          v-tooltip.top="isMinimized ? 'تكبير' : 'تصغير'"
        />
        <Button
          icon="pi pi-times"
          size="small"
          text
          rounded
          severity="danger"
          @click="closeConsole"
          v-tooltip.top="'إغلاق'"
        />
      </div>
    </div>

    <!-- ── Log Lines ────────────────────────────────── -->
    <div v-if="!isMinimized" ref="consoleEl" class="console-body">
      <div v-if="!logs.length" class="console-empty">
        <i class="pi pi-spin pi-spinner mr-2"></i>
        انتظر بداية التنفيذ...
      </div>

      <div v-for="log in logs" :key="log.id" class="log-line" :class="levelClass(log.level)">
        <span class="log-time">{{ log.time }}</span>
        <span v-if="log.nodeId" class="log-node">[{{ log.nodeId.slice(0, 8) }}]</span>
        <span class="log-msg">{{ log.message }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.live-console {
  width: 100%;
  background: #0d1117;
  border-top: 1px solid #21262d; /* ✅ separator بين الـ components */
  font-family: 'Fira Code', 'Consolas', monospace;
  /* ❌ شيل: position, bottom, left, right, z-index */
}

.live-console--minimized .console-body {
  display: none;
}

.console-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 6px 12px;
  background: #161b22;
  border-bottom: 1px solid #21262d;
  user-select: none;
}

.console-header__left,
.console-header__right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.console-title {
  font-size: 0.8rem;
  font-weight: 600;
  color: #c9d1d9;
}

.console-body {
  height: 180px; /* ✅ fixed height — مش 200px عشان يضغط على الـ bottom strip */
  overflow-y: auto;
  padding: 8px 12px;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

/* باقي الـ styles زي ما هي */
.console-empty {
  color: #6e7681;
  font-size: 0.8rem;
  text-align: center;
  padding: 40px 0;
}
.log-line {
  display: flex;
  gap: 8px;
  font-size: 0.78rem;
  line-height: 1.5;
  padding: 1px 0;
}
.log-time {
  color: #6e7681;
  flex-shrink: 0;
  font-size: 0.7rem;
}
.log-node {
  color: #388bfd;
  flex-shrink: 0;
  font-size: 0.7rem;
}
.log-msg {
  flex: 1;
  word-break: break-all;
}
.log-info .log-msg {
  color: #c9d1d9;
}
.log-success .log-msg {
  color: #3fb950;
}
.log-error .log-msg {
  color: #f85149;
}
.log-warn .log-msg {
  color: #d29922;
}
</style>
