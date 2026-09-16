<!-- <script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'

const logs = ref([])

const status = ref('connecting')

const consoleEl = ref(null)

const isMinimized = ref(false)

const ws = ref(null)

const maxLines = 500

const DEBUG_ENABLED = import.meta.env.VITE_DEBUG_CONSOLE === 'true'

const WS_URL = import.meta.env.VITE_DEBUG_WS_URL || 'ws://127.0.0.1:8000/ws/debug/'

// ===================================================
// Add Log
// ===================================================

const addLog = (level, message, logger = null, timestamp = null) => {
  logs.value.push({
    id: Date.now() + Math.random(),

    level,

    message,

    logger,

    timestamp: timestamp || Date.now(),

    time: new Date(timestamp ? timestamp * 1000 : Date.now()).toLocaleTimeString('ar-EG', {
      hour12: false,
    }),
  })

  if (logs.value.length > maxLines) {
    logs.value = logs.value.slice(-maxLines)
  }

  nextTick(() => {
    if (consoleEl.value) {
      consoleEl.value.scrollTop = consoleEl.value.scrollHeight
    }
  })
}

// ===================================================
// Connect WebSocket
// ===================================================

const connect = () => {
  if (!DEBUG_ENABLED) {
    status.value = 'disabled'

    return
  }

  ws.value = new WebSocket(WS_URL)

  ws.value.onopen = () => {
    status.value = 'connected'

    addLog('success', '🔌 Debug Console connected')
  }

  ws.value.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data)

      addLog(
        data.level || 'info',

        data.message || '',

        data.logger || null,

        data.timestamp || null,
      )
    } catch {
      addLog('info', event.data)
    }
  }

  ws.value.onerror = () => {
    status.value = 'error'

    addLog('error', '❌ WebSocket connection error')
  }

  ws.value.onclose = () => {
    status.value = 'closed'

    addLog('warn', '🔌 Debug Console disconnected')
  }
}

// ===================================================
// Close
// ===================================================

const closeConsole = () => {
  ws.value?.close()
}

// ===================================================
// Clear
// ===================================================

const clearLogs = () => {
  logs.value = []
}

// ===================================================
// Level Class
// ===================================================

const levelClass = (level) => {
  return (
    {
      debug: 'log-debug',

      info: 'log-info',

      warn: 'log-warn',

      error: 'log-error',

      success: 'log-success',
    }[level] || 'log-info'
  )
}

// ===================================================
// Lifecycle
// ===================================================

onMounted(() => {
  connect()
})

onBeforeUnmount(() => {
  ws.value?.close()
})
</script>

<template>
  <div
    v-if="DEBUG_ENABLED"
    class="live-debug-console"
    :class="{
      minimized: isMinimized,
    }"
  >



    <div class="console-header">
      <div>
        <span class="console-title">
          <i class="pi pi-terminal" />

          Live Debug Console
        </span>

        <span class="console-status" :class="status"> ● {{ status }} </span>
      </div>

      <div class="console-actions">
        <button @click="clearLogs">Clear</button>

        <button @click="isMinimized = !isMinimized">
          {{ isMinimized ? '▲' : '▼' }}
        </button>

        <button @click="closeConsole">×</button>
      </div>
    </div>



    <div v-if="!isMinimized" ref="consoleEl" class="console-body">
      <div v-if="!logs.length" class="console-empty">Waiting for Django logs...</div>

      <div v-for="log in logs" :key="log.id" class="log-line" :class="levelClass(log.level)">
        <span class="log-time">
          {{ log.time }}
        </span>

        <span class="log-level">
          {{ log.level.toUpperCase() }}
        </span>

        <span v-if="log.logger" class="log-logger"> [{{ log.logger }}] </span>

        <span class="log-message">
          {{ log.message }}
        </span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.live-debug-console {
  position: fixed;

  left: 20px;

  right: 20px;

  bottom: 20px;

  z-index: 99999;

  background: #07111f;

  border: 1px solid #1e5eff;

  border-radius: 10px;

  color: #e5e7eb;

  font-family: monospace;

  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
}

.console-header {
  display: flex;

  justify-content: space-between;

  align-items: center;

  padding: 12px 16px;

  background: #0b1728;

  border-bottom: 1px solid #1e293b;
}

.console-title {
  font-weight: 700;

  margin-right: 15px;
}

.console-status {
  font-size: 12px;
}

.console-status.connected {
  color: #22c55e;
}

.console-status.error {
  color: #ef4444;
}

.console-status.closed {
  color: #f59e0b;
}

.console-actions {
  display: flex;

  gap: 6px;
}

.console-actions button {
  border: 0;

  background: #17243a;

  color: white;

  padding: 5px 10px;

  border-radius: 5px;

  cursor: pointer;
}

.console-body {
  height: 300px;

  overflow-y: auto;

  padding: 12px;
}

.console-empty {
  color: #64748b;

  text-align: center;

  padding: 50px;
}

.log-line {
  display: flex;

  gap: 10px;

  padding: 4px 0;

  font-size: 13px;

  line-height: 1.5;
}

.log-time {
  color: #64748b;

  min-width: 75px;
}

.log-level {
  min-width: 65px;

  font-weight: bold;
}

.log-logger {
  color: #38bdf8;
}

.log-message {
  white-space: pre-wrap;
}

.log-info {
  color: #60a5fa;
}

.log-debug {
  color: #a78bfa;
}

.log-warn {
  color: #fbbf24;
}

.log-error {
  color: #f87171;
}

.log-success {
  color: #4ade80;
}

.minimized .console-body {
  display: none;
}
</style> -->

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'

/*
|--------------------------------------------------------------------------
| Debug Console
|--------------------------------------------------------------------------
*/

const logs = ref([])
const status = ref('connecting')
const consoleEl = ref(null)
const isMinimized = ref(false)
const ws = ref(null)

const maxLines = 500

/*
|--------------------------------------------------------------------------
| Environment
|--------------------------------------------------------------------------
*/

const DEBUG_ENABLED = String(import.meta.env.VITE_DEBUG_CONSOLE).toLowerCase() === 'true'

const WS_URL = import.meta.env.VITE_DEBUG_WS_URL || 'ws://127.0.0.1:8000/ws/debug/'

/*
|--------------------------------------------------------------------------
| Add Log
|--------------------------------------------------------------------------
*/

const addLog = (level, message, logger = null, timestamp = null) => {
  logs.value.push({
    id: Date.now() + Math.random(),
    level,
    message,
    logger,
    timestamp: timestamp || Date.now(),
    time: new Date(timestamp ? timestamp * 1000 : Date.now()).toLocaleTimeString('ar-EG', {
      hour12: false,
    }),
  })

  if (logs.value.length > maxLines) {
    logs.value = logs.value.slice(-maxLines)
  }

  nextTick(() => {
    if (consoleEl.value) {
      consoleEl.value.scrollTop = consoleEl.value.scrollHeight
    }
  })
}

/*
|--------------------------------------------------------------------------
| Connect WebSocket
|--------------------------------------------------------------------------
*/

const connect = () => {
  /*
   * لا نخفي الـ Console.
   * حتى لو DEBUG_ENABLED = false
   * نريد معرفة السبب من داخل المتصفح.
   */

  status.value = 'connecting'

  addLog('info', `VITE_DEBUG_CONSOLE = ${String(import.meta.env.VITE_DEBUG_CONSOLE)}`)

  addLog('info', `WebSocket URL = ${WS_URL}`)

  if (!DEBUG_ENABLED) {
    status.value = 'disabled'

    addLog('warn', '⚠️ Debug Console disabled: VITE_DEBUG_CONSOLE is not true')

    return
  }

  try {
    ws.value = new WebSocket(WS_URL)

    ws.value.onopen = () => {
      status.value = 'connected'

      addLog('success', '🔌 Debug Console connected')
    }

    ws.value.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)

        addLog(
          data.level || 'info',
          data.message || '',
          data.logger || null,
          data.timestamp || null,
        )
      } catch {
        addLog('info', event.data)
      }
    }

    ws.value.onerror = () => {
      status.value = 'error'

      addLog('error', `❌ WebSocket connection error: ${WS_URL}`)
    }

    ws.value.onclose = (event) => {
      status.value = 'closed'

      addLog('warn', `🔌 Debug Console disconnected | code=${event.code}`)
    }
  } catch (error) {
    status.value = 'error'

    addLog('error', `❌ WebSocket exception: ${error.message}`)
  }
}

/*
|--------------------------------------------------------------------------
| Close
|--------------------------------------------------------------------------
*/

const closeConsole = () => {
  if (ws.value) {
    ws.value.close()
  }

  status.value = 'closed'
}

/*
|--------------------------------------------------------------------------
| Clear
|--------------------------------------------------------------------------
*/

const clearLogs = () => {
  logs.value = []
}

/*
|--------------------------------------------------------------------------
| Level Class
|--------------------------------------------------------------------------
*/

const levelClass = (level) => {
  return (
    {
      debug: 'log-debug',
      info: 'log-info',
      warn: 'log-warn',
      error: 'log-error',
      success: 'log-success',
    }[level] || 'log-info'
  )
}

/*
|--------------------------------------------------------------------------
| Lifecycle
|--------------------------------------------------------------------------
*/

onMounted(() => {
  connect()
})

onBeforeUnmount(() => {
  if (ws.value) {
    ws.value.close()
  }
})
</script>

<template>
  <!--
    مهم:
    لا نستخدم v-if="DEBUG_ENABLED" هنا.
    الـ Console لازم يفضل ظاهر حتى لو WebSocket فيه مشكلة.
  -->

  <div
    class="live-debug-console"
    :class="{
      minimized: isMinimized,
    }"
  >
    <!-- Header -->
    <div class="console-header">
      <div class="console-header-info">
        <span class="console-title">
          <i class="pi pi-terminal" />
          Live Debug Console
        </span>

        <span class="console-status" :class="status"> ● {{ status }} </span>
      </div>

      <div class="console-actions">
        <button type="button" @click="clearLogs">Clear</button>

        <button type="button" @click="isMinimized = !isMinimized">
          {{ isMinimized ? '▲' : '▼' }}
        </button>

        <button type="button" @click="closeConsole">×</button>
      </div>
    </div>

    <!-- Logs -->
    <div v-if="!isMinimized" ref="consoleEl" class="console-body">
      <div v-if="!logs.length" class="console-empty">Waiting for Django logs...</div>

      <div v-for="log in logs" :key="log.id" class="log-line" :class="levelClass(log.level)">
        <span class="log-time">
          {{ log.time }}
        </span>

        <span class="log-level">
          {{ log.level.toUpperCase() }}
        </span>

        <span v-if="log.logger" class="log-logger"> [{{ log.logger }}] </span>

        <span class="log-message">
          {{ log.message }}
        </span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.live-debug-console {
  position: fixed;
  left: 20px;
  right: 20px;
  bottom: 20px;

  z-index: 2147483647;

  background: #07111f;

  border: 1px solid #1e5eff;

  border-radius: 10px;

  color: #e5e7eb;

  font-family: monospace;

  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
}

.console-header {
  display: flex;

  justify-content: space-between;

  align-items: center;

  padding: 12px 16px;

  background: #0b1728;

  border-bottom: 1px solid #1e293b;
}

.console-header-info {
  display: flex;

  align-items: center;

  gap: 15px;
}

.console-title {
  font-weight: 700;
}

.console-status {
  font-size: 12px;
}

.console-status.connected {
  color: #22c55e;
}

.console-status.connecting {
  color: #38bdf8;
}

.console-status.error {
  color: #ef4444;
}

.console-status.closed {
  color: #f59e0b;
}

.console-status.disabled {
  color: #f59e0b;
}

.console-actions {
  display: flex;

  gap: 6px;
}

.console-actions button {
  border: 0;

  background: #17243a;

  color: white;

  padding: 5px 10px;

  border-radius: 5px;

  cursor: pointer;
}

.console-actions button:hover {
  background: #263957;
}

.console-body {
  height: 300px;

  overflow-y: auto;

  padding: 12px;
}

.console-empty {
  color: #64748b;

  text-align: center;

  padding: 50px;
}

.log-line {
  display: flex;

  gap: 10px;

  padding: 4px 0;

  font-size: 13px;

  line-height: 1.5;
}

.log-time {
  color: #64748b;

  min-width: 75px;
}

.log-level {
  min-width: 65px;

  font-weight: bold;
}

.log-logger {
  color: #38bdf8;
}

.log-message {
  white-space: pre-wrap;

  word-break: break-word;
}

.log-info {
  color: #60a5fa;
}

.log-debug {
  color: #a78bfa;
}

.log-warn {
  color: #fbbf24;
}

.log-error {
  color: #f87171;
}

.log-success {
  color: #4ade80;
}

.minimized .console-body {
  display: none;
}
</style>
