<!-- <script setup>
import { ref, computed, onMounted, onBeforeUnmount, nextTick } from 'vue'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import { DEBUG_WS_URL } from '@/services/Shared/apiConfig'

// --- Configuration ---
// تفعيل الكونسول تلقائياً في بيئة التطوير فقط أو عند تفعيل المتغير صراحة
const enabled = import.meta.env.DEV || import.meta.env.VITE_DEBUG_CONSOLE === 'true'
const wsEnabled = import.meta.env.VITE_DEBUG_CONSOLE === 'true'
const WS_URL = DEBUG_WS_URL
const MAX_LOGS = 500

// --- UI States ---
const open = ref(false)
const minimized = ref(false)
const paused = ref(false)
const autoScroll = ref(true)
const searchQuery = ref('')
const activeFilter = ref('all') // 'all' | 'error' | 'warn' | 'network' | 'pinia'

// --- Telemetry & Socket States ---
const logs = ref([])
const status = ref('closed') // 'connecting' | 'connected' | 'closed' | 'error'
let ws = null
let reconnectTimer = null
let toastTimer = null

const frontendConsoleEl = ref(null)
const backendConsoleEl = ref(null)
const toastMessage = ref('')
const showToastFlag = ref(false)

// --- Filter Tabs Definition (DRY) ---
const filterTabs = [
  { id: 'all', label: 'All Events' },
  { id: 'error', label: 'Errors' },
  { id: 'warn', label: 'Warnings' },
  { id: 'network', label: 'Network & API' },
  { id: 'pinia', label: 'Pinia / State' },
]

// --- Toast Notification Helper ---
function showToast(msg) {
  toastMessage.value = msg
  showToastFlag.value = true
  clearTimeout(toastTimer)
  toastTimer = setTimeout(() => {
    showToastFlag.value = false
  }, 2400)
}

// --- Clipboard Copy Helper ---
async function copyToClipboard(text, successMsg = 'تم النسخ إلى الحافظة بنجاح') {
  try {
    await navigator.clipboard.writeText(text)
    showToast(successMsg)
  } catch {
    showToast('فشل النسخ إلى الحافظة')
  }
}

// --- Add Log Entry ---
const addLog = (entry) => {
  if (paused.value) return

  const normalizedSource = (entry.source || 'APP').toUpperCase()
  const normalizedLevel = (entry.level || 'info').toLowerCase()
  const formattedPayload = entry.payload ? JSON.stringify(entry.payload, null, 2) : null

  const newEntry = {
    id: crypto.randomUUID ? crypto.randomUUID() : `${Date.now()}-${Math.random()}`,
    time:
      entry.time ||
      new Date().toLocaleTimeString('en-GB', { hour12: false, fractionalSecondDigits: 3 }),
    level: normalizedLevel,
    source: normalizedSource,
    message: entry.message || '',
    payload: entry.payload || null,
    formattedPayload,
    // تجهيز نص البحث مسبقاً لتسريع الفلترة
    searchableText:
      `${entry.message || ''} ${normalizedSource} ${formattedPayload || ''}`.toLowerCase(),
    // تم إصلاح الخطأ هنا بمقارنة الأحرف الكبيرة
    isBackend: ['DJANGO', 'SQL', 'CELERY', 'BACKEND'].includes(normalizedSource),
  }

  logs.value.push(newEntry)
  if (logs.value.length > MAX_LOGS) {
    logs.value.shift()
  }

  if (autoScroll.value && !minimized.value) {
    nextTick(() => {
      const targetEl = newEntry.isBackend ? backendConsoleEl.value : frontendConsoleEl.value
      if (targetEl) {
        targetEl.scrollTop = targetEl.scrollHeight
      }
    })
  }
}

// --- WebSocket Connection with Auto-Reconnect ---
function connect() {
  if (!enabled || !wsEnabled || !open.value || ws) return

  clearTimeout(reconnectTimer)
  status.value = 'connecting'

  try {
    ws = new WebSocket(WS_URL)

    ws.onopen = () => {
      status.value = 'connected'
      addLog({
        level: 'success',
        message: 'Connected to Django Debug Kernel',
        source: 'WEBSOCKET',
      })
    }

    ws.onmessage = (e) => {
      try {
        const d = JSON.parse(e.data)
        addLog({
          level: d.level || 'info',
          message: d.message || '',
          source: d.source || 'DJANGO',
          payload: d,
        })
      } catch {
        addLog({ level: 'info', message: e.data, source: 'DJANGO' })
      }
    }

    ws.onerror = () => {
      status.value = 'error'
    }

    ws.onclose = () => {
      status.value = 'closed'
      ws = null
      // إعادة الاتصال تلقائياً بعد 3 ثوانٍ إذا كانت اللوحة لا تزال مفتوحة
      if (open.value) {
        reconnectTimer = setTimeout(connect, 3000)
      }
    }
  } catch {
    status.value = 'error'
  }
}

function disconnect() {
  clearTimeout(reconnectTimer)
  if (ws) {
    ws.onclose = null // منع إعادة الاتصال عند الإغلاق اليدوي
    ws.close()
    ws = null
  }
  status.value = 'closed'
}

function toggle() {
  open.value = !open.value
  localStorage.setItem('debug_console_open', String(open.value))
  if (open.value) connect()
  else disconnect()
}

// --- Event Listeners (API & Keyboard Shortcut) ---
function onApi(e) {
  const d = e.detail || {}
  addLog({
    level: d.phase === 'error' ? 'error' : d.phase === 'response' ? 'success' : 'info',
    source: 'API',
    message: `${d.method || ''} ${d.url || ''}`.trim(),
    payload: d,
  })
}

function onKeydown(e) {
  // اختصار Ctrl + Shift + D لفتح وإغلاق الكونسول بسرعة
  if (e.ctrlKey && e.shiftKey && e.key.toLowerCase() === 'd') {
    e.preventDefault()
    toggle()
  }
}

// --- Actions ---
function clearLogs() {
  logs.value = []
  showToast('تم تفريغ السجلات بنجاح')
}

function copyAllConsole() {
  if (!logs.value.length) return showToast('لا توجد سجلات لنسخها')
  const text = logs.value
    .map(
      (x) =>
        `[${x.time}] [${x.source}] [${x.level.toUpperCase()}]: ${x.message}${
          x.formattedPayload ? `\nPayload:\n${x.formattedPayload}` : ''
        }`,
    )
    .join('\n' + '-'.repeat(40) + '\n')
  copyToClipboard(text, 'تم نسخ كافة السجلات بنجاح')
}

// --- Computed Filtered Logs ---
const filteredLogs = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()

  return logs.value.filter((log) => {
    if (q && !log.searchableText.includes(q)) return false

    switch (activeFilter.value) {
      case 'error':
        return log.level === 'error'
      case 'warn':
        return log.level === 'warn' || log.level === 'warning'
      case 'network':
        return log.source === 'API' || log.source === 'WEBSOCKET'
      case 'pinia':
        return log.source.includes('PINIA') || log.searchableText.includes('pinia')
      default:
        return true
    }
  })
})

const clientLogs = computed(() => filteredLogs.value.filter((l) => !l.isBackend))
const backendLogs = computed(() => filteredLogs.value.filter((l) => l.isBackend))
const errorCount = computed(() => logs.value.filter((l) => l.level === 'error').length)

// --- Lifecycle ---
onMounted(() => {
  if (!enabled) return
  open.value = localStorage.getItem('debug_console_open') === 'true'
  window.addEventListener('so-iam-api-log', onApi)
  window.addEventListener('keydown', onKeydown)
  if (open.value) connect()
})

onBeforeUnmount(() => {
  window.removeEventListener('so-iam-api-log', onApi)
  window.removeEventListener('keydown', onKeydown)
  clearTimeout(toastTimer)
  disconnect()
})
</script>

<template>
  <div v-if="enabled" class="fixed left-5 bottom-5 z-[99999] font-body-md" dir="ltr">

    <Button
      severity="secondary"
      size="small"
      class="flex items-center gap-2 bg-surface-container-lowest text-on-surface border border-outline-variant rounded-xl px-4 py-2.5 shadow-2xl hover:bg-surface-container-high transition-all"
      @click="toggle"
      title="Toggle Debug Console (Ctrl+Shift+D)"
    >
      <span class="font-label-md text-label-md">Debug Console</span>
      <span
        v-if="errorCount > 0"
        class="px-1.5 py-0.2 text-[10px] font-bold rounded-full bg-error text-on-error"
      >
        {{ errorCount }}
      </span>
      <span
        class="w-2 h-2 rounded-full"
        :class="{
          'bg-tertiary animate-pulse': status === 'connected',
          'bg-secondary animate-bounce': status === 'connecting',
          'bg-error': status === 'closed' || status === 'error',
        }"
      ></span>
    </Button>


    <div
      v-if="open"
      class="fixed inset-x-4 bottom-16 md:inset-x-8 md:bottom-20 max-w-[96vw] mx-auto bg-surface-container-lowest border border-outline-variant rounded-2xl shadow-[0_25px_60px_rgba(0,0,0,0.8)] flex flex-col overflow-hidden z-[100000] backdrop-blur-2xl transition-all duration-200"
      :class="minimized ? 'h-14' : 'h-[82vh] max-h-[760px]'"
    >

      <div
        class="px-4 py-2.5 bg-surface-container-low border-b border-outline-variant flex flex-wrap items-center justify-between gap-3"
      >
        <div class="flex items-center gap-3">
          <div
            class="w-8 h-8 rounded-lg bg-surface-container flex items-center justify-center text-primary shadow-sm"
          >
            <span class="material-symbols-outlined text-[18px]">terminal</span>
          </div>
          <div>
            <div class="flex items-center gap-2">
              <span class="font-headline-sm text-headline-sm text-on-surface font-semibold">
                Live Debug Console
              </span>
              <span
                class="px-1.5 py-0.5 rounded bg-surface-container-high text-primary font-code-sm text-[10px] font-semibold"
              >
                Ctrl+Shift+D
              </span>
            </div>
            <span class="font-body-sm text-[11px] text-outline block">
              Real-time bidirectional telemetry (Socket:
              <strong class="uppercase">{{ status }}</strong
              >)
            </span>
          </div>
        </div>


        <div class="flex flex-wrap items-center gap-1.5">
          <Button
            text
            size="small"
            class="flex items-center gap-1.5 text-on-surface-variant hover:text-on-surface"
            @click="autoScroll = !autoScroll"
          >
            <span
              class="w-2 h-2 rounded-full"
              :class="
                autoScroll ? 'bg-tertiary shadow-[0_0_8px_rgba(78,222,163,0.8)]' : 'bg-outline'
              "
            ></span>
            <span class="text-label-sm">Auto-Scroll</span>
          </Button>

          <Button
            text
            size="small"
            class="flex items-center gap-1.5 text-on-surface-variant hover:text-on-surface"
            @click="paused = !paused"
          >
            <span class="material-symbols-outlined text-[16px]">
              {{ paused ? 'play_arrow' : 'pause' }}
            </span>
            <span class="text-label-sm">{{ paused ? 'Resume' : 'Pause' }}</span>
          </Button>

          <Button
            text
            size="small"
            class="flex items-center gap-1.5 text-on-surface-variant hover:text-error"
            @click="clearLogs"
          >
            <span class="material-symbols-outlined text-[16px]">delete_sweep</span>
            <span class="text-label-sm">Clear</span>
          </Button>

          <Button
            size="small"
            class="bg-primary text-on-primary font-medium shadow-sm hover:bg-primary-container flex items-center gap-1.5"
            @click="copyAllConsole"
          >
            <span class="material-symbols-outlined text-[16px]">content_copy</span>
            <span class="text-label-sm">Copy All</span>
          </Button>

          <div class="flex items-center gap-1 pl-2 border-l border-outline-variant/50">
            <Button
              text
              size="small"
              class="text-outline hover:text-on-surface"
              @click="minimized = !minimized"
            >
              <span class="material-symbols-outlined text-[18px]">
                {{ minimized ? 'open_in_full' : 'minimize' }}
              </span>
            </Button>
            <Button text size="small" class="text-outline hover:text-error" @click="toggle">
              <span class="material-symbols-outlined text-[18px]">close</span>
            </Button>
          </div>
        </div>
      </div>


      <div
        v-if="!minimized"
        class="px-4 py-2 bg-surface-container border-b border-outline-variant/60 flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3"
      >
        <div class="flex items-center gap-1 overflow-x-auto py-0.5">
          <Button
            v-for="tab in filterTabs"
            :key="tab.id"
            size="small"
            :text="activeFilter !== tab.id"
            class="whitespace-nowrap"
            :class="activeFilter === tab.id ? 'font-semibold' : 'text-on-surface-variant'"
            :severity="
              activeFilter === tab.id && tab.id === 'error'
                ? 'danger'
                : activeFilter === tab.id && tab.id === 'warn'
                  ? 'warn'
                  : undefined
            "
            :label="tab.id === 'all' ? `${tab.label} (${logs.length})` : tab.label"
            @click="activeFilter = tab.id"
          />
        </div>


        <IconField class="w-full md:max-w-xs">
          <InputIcon class="material-symbols-outlined text-[16px] text-outline">search</InputIcon>
          <InputText
            v-model="searchQuery"
            size="small"
            class="w-full bg-surface-container-low border border-outline-variant/40 text-on-surface text-code-sm rounded-lg"
            placeholder="Filter logs or payload..."
          />
        </IconField>
      </div>


      <div
        v-if="!minimized"
        class="grid grid-cols-1 lg:grid-cols-2 flex-1 overflow-hidden divide-y lg:divide-y-0 lg:divide-x divide-outline-variant/50 bg-surface"
      >

        <section
          v-for="panel in [
            {
              key: 'client',
              title: 'CLIENT RUNTIME (Frontend)',
              icon: 'devices',
              iconColor: 'text-tertiary',
              items: clientLogs,
              emptyText: 'Waiting for frontend client events...',
              setRef: (el) => (frontendConsoleEl = el),
            },
            {
              key: 'backend',
              title: 'BACKEND ENGINE & APIS (Django)',
              icon: 'dns',
              iconColor: 'text-primary',
              items: backendLogs,
              emptyText: 'Waiting for Django backend & API logs...',
              setRef: (el) => (backendConsoleEl = el),
            },
          ]"
          :key="panel.key"
          class="flex flex-col h-full overflow-hidden bg-surface-container-lowest/40"
        >
          <div
            class="px-4 py-2 bg-surface-container-low/80 border-b border-outline-variant/40 flex items-center justify-between"
          >
            <div class="flex items-center gap-2">
              <span class="material-symbols-outlined text-[16px]" :class="panel.iconColor">
                {{ panel.icon }}
              </span>
              <span class="font-headline-sm text-label-md text-on-surface font-semibold">
                {{ panel.title }}
              </span>
            </div>
            <span class="font-code-sm text-[10px] text-outline">
              {{ panel.items.length }} events
            </span>
          </div>

          <div
            :ref="panel.setRef"
            class="flex-1 overflow-y-auto p-3 font-code-sm text-code-sm space-y-2 select-text"
          >
            <div
              v-if="!panel.items.length"
              class="h-full flex items-center justify-center text-outline italic text-xs"
            >
              {{ panel.emptyText }}
            </div>

            <div
              v-for="log in panel.items"
              :key="log.id"
              class="group p-2.5 rounded-lg bg-surface-container-low/60 hover:bg-surface-container transition-colors flex flex-col gap-1.5 border border-outline-variant/20"
              :class="{ 'bg-error-container/15 border-error/30': log.level === 'error' }"
            >
              <div class="flex items-center justify-between gap-2">
                <div class="flex items-center gap-2 flex-wrap min-w-0">
                  <span class="text-outline text-[10px]">{{ log.time }}</span>
                  <span
                    class="px-1.5 py-0.5 rounded font-semibold text-[10px] tracking-wide uppercase"
                    :class="{
                      'bg-primary-container/40 text-primary':
                        log.level === 'info' || log.level === 'success',
                      'bg-error-container text-error': log.level === 'error',
                      'bg-secondary-container/30 text-secondary':
                        log.level === 'warn' || log.level === 'warning',
                      'bg-tertiary-container/30 text-tertiary': log.level === 'debug',
                    }"
                  >
                    {{ panel.key === 'backend' ? log.source : log.level }}
                  </span>
                  <span class="text-on-surface font-medium truncate">{{ log.message }}</span>
                </div>

                <Button
                  text
                  rounded
                  size="small"
                  class="opacity-0 group-hover:opacity-100 transition-opacity text-outline hover:text-on-surface"
                  title="نسخ السجل"
                  @click="copyToClipboard(log.formattedPayload || log.message)"
                >
                  <span class="material-symbols-outlined text-[14px]">content_copy</span>
                </Button>
              </div>

              <div
                v-if="log.formattedPayload"
                class="mt-1 pl-3 bg-surface-container-lowest rounded p-2 overflow-x-auto border border-outline-variant/20"
              >
                <pre
                  class="text-[11px] font-code-sm leading-relaxed text-on-surface-variant whitespace-pre-wrap"
                  >{{ log.formattedPayload }}</pre>
              </div>
            </div>
          </div>
        </section>
      </div>


      <div
        v-if="!minimized"
        class="px-4 py-2 bg-surface-container-low border-t border-outline-variant/60 flex flex-wrap items-center justify-between gap-3 text-code-sm font-code-sm text-outline"
      >
        <div class="flex items-center gap-4">
          <div class="flex items-center gap-1.5">
            <span
              class="w-2 h-2 rounded-full"
              :class="status === 'connected' ? 'bg-tertiary' : 'bg-error'"
            ></span>
            <span>
              STATUS: <strong class="text-on-surface uppercase">{{ status }}</strong>
            </span>
          </div>
          <div class="hidden sm:inline">|</div>
          <div class="hidden sm:flex items-center gap-1">
            <span>TOTAL LOGS:</span>
            <strong class="text-primary">{{ logs.length }}</strong>
          </div>
        </div>
        <div class="text-[11px] text-outline">
          So_Iam_OS Developer Command Center • Dual-Pipe Sync Active
        </div>
      </div>
    </div>


    <div
      class="fixed bottom-6 right-6 z-[100001] flex items-center gap-2 px-4 py-2.5 rounded-xl bg-surface-container-highest text-on-surface shadow-2xl transition-all duration-300 border border-outline-variant"
      :class="
        showToastFlag
          ? 'opacity-100 translate-y-0 pointer-events-auto'
          : 'opacity-0 translate-y-4 pointer-events-none'
      "
    >
      <span class="material-symbols-outlined text-tertiary text-[18px]">check_circle</span>
      <span class="font-label-md text-label-md">{{ toastMessage }}</span>
    </div>
  </div>
</template> -->
<script setup>
import { ref, computed, onMounted, onBeforeUnmount, nextTick } from 'vue'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import { DEBUG_WS_URL } from '@/services/Shared/apiConfig'

// --- Configuration ---
// تفعيل الكونسول تلقائياً في بيئة التطوير فقط أو عند تفعيل المتغير صراحة
const enabled = import.meta.env.DEV || import.meta.env.VITE_DEBUG_CONSOLE === 'true'
const wsEnabled = import.meta.env.VITE_DEBUG_CONSOLE === 'true'
const WS_URL = DEBUG_WS_URL
const MAX_LOGS = 500

// --- UI States ---
const open = ref(false)
const minimized = ref(false)
const paused = ref(false)
const autoScroll = ref(true)
const searchQuery = ref('')
const activeFilter = ref('all') // 'all' | 'error' | 'warn' | 'network' | 'pinia'
const expandedIds = ref(new Set())

// --- Telemetry & Socket States ---
const logs = ref([])
const status = ref('closed') // 'connecting' | 'connected' | 'closed' | 'error'
let ws = null
let reconnectTimer = null
let toastTimer = null

const frontendConsoleEl = ref(null)
const backendConsoleEl = ref(null)
const toastMessage = ref('')
const toastType = ref('success') // 'success' | 'error' | 'info'
const showToastFlag = ref(false)

// --- Filter Tabs Definition (DRY + Icons) ---
const filterTabs = [
  { id: 'all', label: 'All Events', icon: 'layers' },
  { id: 'error', label: 'Errors', icon: 'error' },
  { id: 'warn', label: 'Warnings', icon: 'warning' },
  { id: 'network', label: 'Network & API', icon: 'sync_alt' },
  { id: 'pinia', label: 'Pinia / State', icon: 'database' },
]

// --- Toast Notification Helper ---
function showToast(msg, type = 'success') {
  toastMessage.value = msg
  toastType.value = type
  showToastFlag.value = true
  clearTimeout(toastTimer)
  toastTimer = setTimeout(() => {
    showToastFlag.value = false
  }, 2400)
}

// --- Clipboard Copy Helper ---
async function copyToClipboard(text, successMsg = 'تم النسخ إلى الحافظة بنجاح') {
  try {
    await navigator.clipboard.writeText(text)
    showToast(successMsg, 'success')
  } catch {
    showToast('فشل النسخ إلى الحافظة', 'error')
  }
}

// --- Payload Expand / Collapse Helpers ---
function isExpanded(id) {
  return expandedIds.value.has(id)
}

function togglePayload(id) {
  const next = new Set(expandedIds.value)
  if (next.has(id)) next.delete(id)
  else next.add(id)
  expandedIds.value = next
}

function expandAllPayloads() {
  const next = new Set()
  filteredLogs.value.forEach((l) => {
    if (l.formattedPayload) next.add(l.id)
  })
  expandedIds.value = next
  showToast('تم توسيع جميع البيانات التفصيلية', 'info')
}

function collapseAllPayloads() {
  expandedIds.value = new Set()
  showToast('تم طي جميع البيانات التفصيلية', 'info')
}

// --- Extract Helpful API Meta (Status / Duration) if Present ---
function extractMetaBadge(payload) {
  if (!payload || typeof payload !== 'object') return null
  const statusCode = payload.status ?? payload.statusCode ?? payload.response?.status
  const duration = payload.durationMs ?? payload.duration ?? payload.elapsedMs
  const parts = []
  if (statusCode !== undefined && statusCode !== null) parts.push(`HTTP ${statusCode}`)
  if (duration !== undefined && duration !== null) parts.push(`${duration}ms`)
  return parts.length ? parts.join(' • ') : null
}

// --- Level Visual Config ---
function getLevelMeta(level) {
  switch (level) {
    case 'error':
      return {
        icon: 'cancel',
        badgeClass: 'bg-error-container text-error border border-error/25',
      }
    case 'warn':
    case 'warning':
      return {
        icon: 'warning',
        badgeClass: 'bg-secondary-container/30 text-secondary border border-secondary/25',
      }
    case 'success':
      return {
        icon: 'check_circle',
        badgeClass: 'bg-tertiary-container/30 text-tertiary border border-tertiary/25',
      }
    case 'debug':
      return {
        icon: 'bug_report',
        badgeClass:
          'bg-surface-container-high text-on-surface-variant border border-outline-variant/40',
      }
    default:
      return {
        icon: 'info',
        badgeClass: 'bg-primary-container/35 text-primary border border-primary/25',
      }
  }
}

function scrollPanelToBottom(panelKey) {
  nextTick(() => {
    const el = panelKey === 'backend' ? backendConsoleEl.value : frontendConsoleEl.value
    if (el) el.scrollTop = el.scrollHeight
  })
}

// --- Add Log Entry ---
const addLog = (entry) => {
  if (paused.value) return

  const normalizedSource = (entry.source || 'APP').toUpperCase()
  const normalizedLevel = (entry.level || 'info').toLowerCase()
  const formattedPayload = entry.payload ? JSON.stringify(entry.payload, null, 2) : null
  const logId = crypto.randomUUID ? crypto.randomUUID() : `${Date.now()}-${Math.random()}`

  const newEntry = {
    id: logId,
    time:
      entry.time ||
      new Date().toLocaleTimeString('en-GB', { hour12: false, fractionalSecondDigits: 3 }),
    level: normalizedLevel,
    source: normalizedSource,
    message: entry.message || '',
    payload: entry.payload || null,
    formattedPayload,
    metaBadge: extractMetaBadge(entry.payload),
    searchableText:
      `${entry.message || ''} ${normalizedSource} ${formattedPayload || ''}`.toLowerCase(),
    isBackend: ['DJANGO', 'SQL', 'CELERY', 'BACKEND'].includes(normalizedSource),
  }

  logs.value.push(newEntry)
  if (logs.value.length > MAX_LOGS) {
    const removed = logs.value.shift()
    if (removed && expandedIds.value.has(removed.id)) {
      const next = new Set(expandedIds.value)
      next.delete(removed.id)
      expandedIds.value = next
    }
  }

  // توسيع الأخطاء تلقائياً لتسهيل رؤيتها
  if (normalizedLevel === 'error' && formattedPayload) {
    const next = new Set(expandedIds.value)
    next.add(logId)
    expandedIds.value = next
  }

  if (autoScroll.value && !minimized.value) {
    scrollPanelToBottom(newEntry.isBackend ? 'backend' : 'client')
  }
}

// --- WebSocket Connection with Auto-Reconnect ---
function connect() {
  if (!enabled || !wsEnabled || !open.value || ws) return

  clearTimeout(reconnectTimer)
  status.value = 'connecting'

  try {
    ws = new WebSocket(WS_URL)

    ws.onopen = () => {
      status.value = 'connected'
      addLog({
        level: 'success',
        message: 'Connected to Django Debug Kernel',
        source: 'WEBSOCKET',
      })
    }

    ws.onmessage = (e) => {
      try {
        const d = JSON.parse(e.data)
        addLog({
          level: d.level || 'info',
          message: d.message || '',
          source: d.source || 'DJANGO',
          payload: d,
        })
      } catch {
        addLog({ level: 'info', message: e.data, source: 'DJANGO' })
      }
    }

    ws.onerror = () => {
      status.value = 'error'
    }

    ws.onclose = () => {
      status.value = 'closed'
      ws = null
      if (open.value) {
        reconnectTimer = setTimeout(connect, 3000)
      }
    }
  } catch {
    status.value = 'error'
  }
}

function disconnect() {
  clearTimeout(reconnectTimer)
  if (ws) {
    ws.onclose = null
    ws.close()
    ws = null
  }
  status.value = 'closed'
}

function reconnectNow() {
  disconnect()
  if (open.value) {
    showToast('جاري إعادة الاتصال بالـ Debug Socket...', 'info')
    connect()
  }
}

function toggle() {
  open.value = !open.value
  localStorage.setItem('debug_console_open', String(open.value))
  if (open.value) connect()
  else disconnect()
}

// --- Event Listeners (API & Keyboard Shortcut) ---
function onApi(e) {
  const d = e.detail || {}
  addLog({
    level: d.phase === 'error' ? 'error' : d.phase === 'response' ? 'success' : 'info',
    source: 'API',
    message: `${d.method || ''} ${d.url || ''}`.trim(),
    payload: d,
  })
}

function onKeydown(e) {
  if (e.ctrlKey && e.shiftKey && e.key.toLowerCase() === 'd') {
    e.preventDefault()
    toggle()
  }
}

// --- Actions ---
function clearLogs() {
  logs.value = []
  expandedIds.value = new Set()
  showToast('تم تفريغ السجلات بنجاح', 'success')
}

function copyAllConsole() {
  if (!filteredLogs.value.length) return showToast('لا توجد سجلات لنسخها', 'error')
  const text = filteredLogs.value
    .map(
      (x) =>
        `[${x.time}] [${x.source}] [${x.level.toUpperCase()}]: ${x.message}${
          x.metaBadge ? ` (${x.metaBadge})` : ''
        }${x.formattedPayload ? `\nPayload:\n${x.formattedPayload}` : ''}`,
    )
    .join('\n' + '-'.repeat(40) + '\n')
  copyToClipboard(text, `تم نسخ ${filteredLogs.value.length} سجل بنجاح`)
}

function exportLogsJson() {
  if (!filteredLogs.value.length) return showToast('لا توجد سجلات لتصديرها', 'error')
  const dataStr = JSON.stringify(
    {
      exportedAt: new Date().toISOString(),
      socketStatus: status.value,
      filter: activeFilter.value,
      count: filteredLogs.value.length,
      logs: filteredLogs.value.map(({ searchableText, formattedPayload, ...rest }) => rest),
    },
    null,
    2,
  )
  const blob = new Blob([dataStr], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `so-iam-os-debug-${new Date().toISOString().replace(/[:.]/g, '-')}.json`
  a.click()
  URL.revokeObjectURL(url)
  showToast('تم تصدير ملف السجلات JSON', 'success')
}

// --- Computed Filtered Logs & Counters ---
const filteredLogs = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()

  return logs.value.filter((log) => {
    if (q && !log.searchableText.includes(q)) return false

    switch (activeFilter.value) {
      case 'error':
        return log.level === 'error'
      case 'warn':
        return log.level === 'warn' || log.level === 'warning'
      case 'network':
        return log.source === 'API' || log.source === 'WEBSOCKET'
      case 'pinia':
        return log.source.includes('PINIA') || log.searchableText.includes('pinia')
      default:
        return true
    }
  })
})

const clientLogs = computed(() => filteredLogs.value.filter((l) => !l.isBackend))
const backendLogs = computed(() => filteredLogs.value.filter((l) => l.isBackend))

const counts = computed(() => ({
  all: logs.value.length,
  error: logs.value.filter((l) => l.level === 'error').length,
  warn: logs.value.filter((l) => l.level === 'warn' || l.level === 'warning').length,
  network: logs.value.filter((l) => l.source === 'API' || l.source === 'WEBSOCKET').length,
  pinia: logs.value.filter((l) => l.source.includes('PINIA') || l.searchableText.includes('pinia'))
    .length,
}))

const panels = computed(() => [
  {
    key: 'client',
    title: 'CLIENT RUNTIME (Frontend)',
    icon: 'devices',
    iconColor: 'text-tertiary',
    items: clientLogs.value,
    emptyText: 'Waiting for frontend client events...',
    setRef: (el) => {
      frontendConsoleEl.value = el
    },
  },
  {
    key: 'backend',
    title: 'BACKEND ENGINE & APIS (Django)',
    icon: 'dns',
    iconColor: 'text-primary',
    items: backendLogs.value,
    emptyText: 'Waiting for Django backend & API logs...',
    setRef: (el) => {
      backendConsoleEl.value = el
    },
  },
])

// --- Lifecycle ---
onMounted(() => {
  if (!enabled) return
  open.value = localStorage.getItem('debug_console_open') === 'true'
  window.addEventListener('so-iam-api-log', onApi)
  window.addEventListener('keydown', onKeydown)
  if (open.value) connect()
})

onBeforeUnmount(() => {
  window.removeEventListener('so-iam-api-log', onApi)
  window.removeEventListener('keydown', onKeydown)
  clearTimeout(toastTimer)
  disconnect()
})
</script>

<template>
  <div v-if="enabled" class="fixed left-5 bottom-5 z-[99999] font-body-md" dir="ltr">
    <!-- Floating Trigger Button -->
    <Button
      severity="secondary"
      size="small"
      class="flex items-center gap-2 bg-surface-container-lowest text-on-surface border border-outline-variant rounded-xl px-4 py-2.5 shadow-2xl hover:bg-surface-container-high transition-all"
      @click="toggle"
      title="Toggle Debug Console (Ctrl+Shift+D)"
    >
      <span class="material-symbols-outlined text-[18px] text-primary">bug_report</span>
      <span class="font-label-md text-label-md font-medium">Debug Console</span>
      <span
        v-if="counts.error > 0"
        class="px-1.5 py-0.5 text-[10px] font-bold rounded-full bg-error text-on-error flex items-center gap-0.5"
      >
        <span class="material-symbols-outlined text-[12px]">error</span>
        {{ counts.error }}
      </span>
      <span
        class="w-2.5 h-2.5 rounded-full"
        :class="{
          'bg-tertiary shadow-[0_0_8px_rgba(78,222,163,0.85)] animate-pulse':
            status === 'connected',
          'bg-secondary animate-bounce': status === 'connecting',
          'bg-error': status === 'closed' || status === 'error',
        }"
      ></span>
    </Button>

    <!-- Main Command Center Drawer -->
    <div
      v-if="open"
      class="fixed inset-x-4 bottom-16 md:inset-x-8 md:bottom-20 max-w-[96vw] mx-auto bg-surface-container-lowest border border-outline-variant rounded-2xl shadow-[0_25px_60px_rgba(0,0,0,0.8)] flex flex-col overflow-hidden z-[100000] backdrop-blur-2xl transition-all duration-200"
      :class="minimized ? 'h-14' : 'h-[82vh] max-h-[760px]'"
    >
      <!-- Top Header Bar -->
      <div
        class="px-4 py-2.5 bg-surface-container-low border-b border-outline-variant flex flex-wrap items-center justify-between gap-3"
      >
        <div class="flex items-center gap-3">
          <div
            class="w-8 h-8 rounded-lg bg-surface-container border border-outline-variant/40 flex items-center justify-center text-primary shadow-sm"
          >
            <span class="material-symbols-outlined text-[18px]">terminal</span>
          </div>
          <div>
            <div class="flex items-center gap-2 flex-wrap">
              <span class="font-headline-sm text-headline-sm text-on-surface font-semibold">
                Live Debug Console
              </span>
              <span
                class="px-1.5 py-0.5 rounded bg-surface-container-high text-primary font-code-sm text-[10px] font-semibold flex items-center gap-1"
              >
                <span class="material-symbols-outlined text-[12px]">keyboard</span>
                Ctrl+Shift+D
              </span>
              <span
                v-if="paused"
                class="px-2 py-0.5 rounded-full bg-secondary-container/30 text-secondary text-[10px] font-semibold flex items-center gap-1"
              >
                <span class="material-symbols-outlined text-[12px]">pause_circle</span>
                PAUSED
              </span>
            </div>
            <span class="font-body-sm text-[11px] text-outline flex items-center gap-1.5 mt-0.5">
              <span class="material-symbols-outlined text-[13px]">sensors</span>
              <span>Real-time bidirectional telemetry (Socket:</span>
              <strong
                class="uppercase"
                :class="{
                  'text-tertiary': status === 'connected',
                  'text-secondary': status === 'connecting',
                  'text-error': status === 'closed' || status === 'error',
                }"
              >
                {{ status }}
              </strong>
              <span>)</span>
            </span>
          </div>
        </div>

        <!-- Toolbar Actions -->
        <div class="flex flex-wrap items-center gap-1.5">
          <Button
            v-if="wsEnabled"
            text
            size="small"
            class="flex items-center gap-1 text-on-surface-variant hover:text-primary"
            title="Reconnect WebSocket"
            @click="reconnectNow"
          >
            <span
              class="material-symbols-outlined text-[16px]"
              :class="{ 'animate-spin': status === 'connecting' }"
            >
              refresh
            </span>
            <span class="text-label-sm hidden sm:inline">Reconnect</span>
          </Button>

          <Button
            text
            size="small"
            class="flex items-center gap-1.5 text-on-surface-variant hover:text-on-surface"
            title="Toggle Auto-Scroll"
            @click="autoScroll = !autoScroll"
          >
            <span
              class="material-symbols-outlined text-[16px]"
              :class="autoScroll ? 'text-tertiary' : 'text-outline'"
            >
              {{ autoScroll ? 'vertical_align_bottom' : 'push_pin' }}
            </span>
            <span class="text-label-sm">Auto-Scroll</span>
          </Button>

          <Button
            text
            size="small"
            class="flex items-center gap-1.5 text-on-surface-variant hover:text-on-surface"
            :title="paused ? 'Resume Stream' : 'Pause Stream'"
            @click="paused = !paused"
          >
            <span
              class="material-symbols-outlined text-[16px]"
              :class="paused ? 'text-secondary' : ''"
            >
              {{ paused ? 'play_arrow' : 'pause' }}
            </span>
            <span class="text-label-sm">{{ paused ? 'Resume' : 'Pause' }}</span>
          </Button>

          <Button
            text
            size="small"
            class="flex items-center gap-1.5 text-on-surface-variant hover:text-error"
            title="Clear All Logs"
            @click="clearLogs"
          >
            <span class="material-symbols-outlined text-[16px]">delete_sweep</span>
            <span class="text-label-sm">Clear</span>
          </Button>

          <Button
            text
            size="small"
            class="flex items-center gap-1.5 text-on-surface-variant hover:text-primary"
            title="Export Filtered Logs as JSON"
            @click="exportLogsJson"
          >
            <span class="material-symbols-outlined text-[16px]">download</span>
            <span class="text-label-sm hidden md:inline">Export</span>
          </Button>

          <Button
            size="small"
            class="bg-primary text-on-primary font-medium shadow-sm hover:bg-primary-container flex items-center gap-1.5"
            title="Copy Logs to Clipboard"
            @click="copyAllConsole"
          >
            <span class="material-symbols-outlined text-[16px]">content_copy</span>
            <span class="text-label-sm">Copy All</span>
          </Button>

          <div class="flex items-center gap-1 pl-2 border-l border-outline-variant/50">
            <Button
              text
              size="small"
              class="text-outline hover:text-on-surface"
              :title="minimized ? 'Expand Console' : 'Minimize Console'"
              @click="minimized = !minimized"
            >
              <span class="material-symbols-outlined text-[18px]">
                {{ minimized ? 'open_in_full' : 'minimize' }}
              </span>
            </Button>
            <Button
              text
              size="small"
              class="text-outline hover:text-error"
              title="Close Console"
              @click="toggle"
            >
              <span class="material-symbols-outlined text-[18px]">close</span>
            </Button>
          </div>
        </div>
      </div>

      <!-- Sub-Toolbar: Filters, Payload Controls & Search -->
      <div
        v-if="!minimized"
        class="px-4 py-2 bg-surface-container border-b border-outline-variant/60 flex flex-col lg:flex-row items-stretch lg:items-center justify-between gap-2.5"
      >
        <div class="flex items-center gap-1 overflow-x-auto py-0.5">
          <Button
            v-for="tab in filterTabs"
            :key="tab.id"
            size="small"
            :text="activeFilter !== tab.id"
            class="whitespace-nowrap flex items-center gap-1.5"
            :class="activeFilter === tab.id ? 'font-semibold' : 'text-on-surface-variant'"
            :severity="
              activeFilter === tab.id && tab.id === 'error'
                ? 'danger'
                : activeFilter === tab.id && tab.id === 'warn'
                  ? 'warn'
                  : undefined
            "
            @click="activeFilter = tab.id"
          >
            <span class="material-symbols-outlined text-[15px]">{{ tab.icon }}</span>
            <span>{{ tab.label }}</span>
            <span
              class="px-1.5 py-0.2 rounded-full text-[10px] font-code-sm bg-surface-container-high/80"
            >
              {{ counts[tab.id] ?? 0 }}
            </span>
          </Button>
        </div>

        <div class="flex items-center gap-2 w-full lg:w-auto">
          <!-- Expand / Collapse Payloads -->
          <div class="hidden sm:flex items-center gap-1 border-r border-outline-variant/50 pr-2">
            <Button
              text
              size="small"
              class="text-on-surface-variant hover:text-on-surface p-1.5"
              title="Expand All Payloads"
              @click="expandAllPayloads"
            >
              <span class="material-symbols-outlined text-[16px]">unfold_more</span>
            </Button>
            <Button
              text
              size="small"
              class="text-on-surface-variant hover:text-on-surface p-1.5"
              title="Collapse All Payloads"
              @click="collapseAllPayloads"
            >
              <span class="material-symbols-outlined text-[16px]">unfold_less</span>
            </Button>
          </div>

          <!-- PrimeVue IconField Search -->
          <IconField class="w-full sm:w-64 relative">
            <InputIcon class="material-symbols-outlined text-[16px] text-outline">search</InputIcon>
            <InputText
              v-model="searchQuery"
              size="small"
              class="w-full bg-surface-container-low border border-outline-variant/40 text-on-surface text-code-sm rounded-lg pr-7"
              placeholder="Filter logs or payload..."
            />
            <button
              v-if="searchQuery"
              type="button"
              class="absolute right-2 top-1/2 -translate-y-1/2 text-outline hover:text-on-surface flex items-center"
              title="Clear search"
              @click="searchQuery = ''"
            >
              <span class="material-symbols-outlined text-[15px]">close</span>
            </button>
          </IconField>
        </div>
      </div>

      <!-- Split Screen Content Body -->
      <div
        v-if="!minimized"
        class="grid grid-cols-1 lg:grid-cols-2 flex-1 overflow-hidden divide-y lg:divide-y-0 lg:divide-x divide-outline-variant/50 bg-surface"
      >
        <section
          v-for="panel in panels"
          :key="panel.key"
          class="flex flex-col h-full overflow-hidden bg-surface-container-lowest/40"
        >
          <!-- Panel Header -->
          <div
            class="px-4 py-2 bg-surface-container-low/80 border-b border-outline-variant/40 flex items-center justify-between"
          >
            <div class="flex items-center gap-2">
              <span class="material-symbols-outlined text-[16px]" :class="panel.iconColor">
                {{ panel.icon }}
              </span>
              <span class="font-headline-sm text-label-md text-on-surface font-semibold">
                {{ panel.title }}
              </span>
            </div>
            <div class="flex items-center gap-2">
              <span class="font-code-sm text-[10px] text-outline flex items-center gap-1">
                <span class="material-symbols-outlined text-[13px]">receipt_long</span>
                {{ panel.items.length }} events
              </span>
              <button
                v-if="panel.items.length"
                type="button"
                class="text-outline hover:text-primary flex items-center"
                title="Scroll to bottom"
                @click="scrollPanelToBottom(panel.key)"
              >
                <span class="material-symbols-outlined text-[15px]">arrow_downward</span>
              </button>
            </div>
          </div>

          <!-- Logs List -->
          <div
            :ref="panel.setRef"
            class="flex-1 overflow-y-auto p-3 font-code-sm text-code-sm space-y-2 select-text"
          >
            <div
              v-if="!panel.items.length"
              class="h-full flex flex-col items-center justify-center gap-1.5 text-outline italic text-xs py-8"
            >
              <span class="material-symbols-outlined text-[24px] opacity-60">inbox</span>
              <span>{{ panel.emptyText }}</span>
            </div>

            <div
              v-for="log in panel.items"
              :key="log.id"
              class="group p-2.5 rounded-lg bg-surface-container-low/65 hover:bg-surface-container transition-colors flex flex-col gap-1.5 border border-outline-variant/20"
              :class="{ 'bg-error-container/15 border-error/35': log.level === 'error' }"
            >
              <div class="flex items-center justify-between gap-2">
                <div class="flex items-center gap-2 flex-wrap min-w-0">
                  <span class="text-outline text-[10px] flex items-center gap-0.5 shrink-0">
                    <span class="material-symbols-outlined text-[12px]">schedule</span>
                    {{ log.time }}
                  </span>

                  <span
                    class="px-1.5 py-0.5 rounded font-semibold text-[10px] tracking-wide uppercase flex items-center gap-1 shrink-0"
                    :class="getLevelMeta(log.level).badgeClass"
                  >
                    <span class="material-symbols-outlined text-[12px]">
                      {{ getLevelMeta(log.level).icon }}
                    </span>
                    {{ panel.key === 'backend' ? log.source : log.level }}
                  </span>

                  <span
                    v-if="panel.key === 'backend' && log.level !== 'info'"
                    class="px-1.5 py-0.5 rounded bg-surface-container-high text-[10px] uppercase text-on-surface-variant"
                  >
                    {{ log.level }}
                  </span>

                  <span
                    v-if="log.metaBadge"
                    class="px-1.5 py-0.5 rounded bg-surface-container-high text-primary text-[10px] font-semibold shrink-0"
                  >
                    {{ log.metaBadge }}
                  </span>

                  <span class="text-on-surface font-medium break-all">{{ log.message }}</span>
                </div>

                <div class="flex items-center gap-0.5 shrink-0">
                  <Button
                    v-if="log.formattedPayload"
                    text
                    rounded
                    size="small"
                    class="text-outline hover:text-primary"
                    :title="isExpanded(log.id) ? 'إخفاء البيانات' : 'عرض البيانات'"
                    @click="togglePayload(log.id)"
                  >
                    <span class="material-symbols-outlined text-[15px]">
                      {{ isExpanded(log.id) ? 'expand_less' : 'data_object' }}
                    </span>
                  </Button>

                  <Button
                    text
                    rounded
                    size="small"
                    class="opacity-70 group-hover:opacity-100 transition-opacity text-outline hover:text-on-surface"
                    title="نسخ السجل"
                    @click="copyToClipboard(log.formattedPayload || log.message)"
                  >
                    <span class="material-symbols-outlined text-[14px]">content_copy</span>
                  </Button>
                </div>
              </div>

              <div
                v-if="log.formattedPayload && isExpanded(log.id)"
                class="mt-1 pl-3 bg-surface-container-lowest rounded p-2 overflow-x-auto border border-outline-variant/25"
              >
                <pre
                  class="text-[11px] font-code-sm leading-relaxed text-on-surface-variant whitespace-pre-wrap"
                  >{{ log.formattedPayload }}</pre>
              </div>
            </div>
          </div>
        </section>
      </div>

      <!-- Footer Telemetry Stats Bar -->
      <div
        v-if="!minimized"
        class="px-4 py-2 bg-surface-container-low border-t border-outline-variant/60 flex flex-wrap items-center justify-between gap-3 text-code-sm font-code-sm text-outline"
      >
        <div class="flex items-center gap-3 flex-wrap">
          <div class="flex items-center gap-1.5">
            <span
              class="w-2 h-2 rounded-full"
              :class="status === 'connected' ? 'bg-tertiary' : 'bg-error'"
            ></span>
            <span>
              STATUS: <strong class="text-on-surface uppercase">{{ status }}</strong>
            </span>
          </div>
          <span class="hidden sm:inline">|</span>
          <div class="flex items-center gap-1">
            <span class="material-symbols-outlined text-[14px] text-primary">analytics</span>
            <span>TOTAL:</span>
            <strong class="text-primary">{{ logs.length }}</strong>
          </div>
          <div class="flex items-center gap-1">
            <span class="material-symbols-outlined text-[14px] text-error">error</span>
            <span>ERRORS:</span>
            <strong class="text-error">{{ counts.error }}</strong>
          </div>
          <div class="hidden sm:flex items-center gap-1">
            <span class="material-symbols-outlined text-[14px] text-secondary">warning</span>
            <span>WARNS:</span>
            <strong class="text-secondary">{{ counts.warn }}</strong>
          </div>
        </div>

        <div class="text-[11px] text-outline flex items-center gap-1">
          <span class="material-symbols-outlined text-[14px] text-tertiary">bolt</span>
          <span>So_Iam_OS Developer Command Center • Dual-Pipe Sync Active</span>
        </div>
      </div>
    </div>

    <!-- Floating Toast Notification -->
    <div
      class="fixed bottom-6 right-6 z-[100001] flex items-center gap-2 px-4 py-2.5 rounded-xl bg-surface-container-highest text-on-surface shadow-2xl transition-all duration-300 border border-outline-variant"
      :class="
        showToastFlag
          ? 'opacity-100 translate-y-0 pointer-events-auto'
          : 'opacity-0 translate-y-4 pointer-events-none'
      "
    >
      <span
        class="material-symbols-outlined text-[18px]"
        :class="{
          'text-tertiary': toastType === 'success',
          'text-error': toastType === 'error',
          'text-primary': toastType === 'info',
        }"
      >
        {{ toastType === 'error' ? 'error' : toastType === 'info' ? 'info' : 'check_circle' }}
      </span>
      <span class="font-label-md text-label-md">{{ toastMessage }}</span>
    </div>
  </div>
</template>
