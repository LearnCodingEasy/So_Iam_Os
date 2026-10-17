<!-- <script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
const open=ref(false), minimized=ref(false), logs=ref([]), status=ref('closed'), ws=ref(null), consoleEl=ref(null)
const enabled=true; const wsEnabled=import.meta.env.VITE_DEBUG_CONSOLE==='true'; const WS_URL=import.meta.env.VITE_DEBUG_WS_URL||'ws://127.0.0.1:8000/ws/debug/'
const addLog=(entry)=>{logs.value=[...logs.value,{id:Date.now()+Math.random(),...entry,time:entry.time||new Date().toLocaleTimeString('ar-EG',{hour12:false})}].slice(-500); nextTick(()=>{if(consoleEl.value)consoleEl.value.scrollTop=consoleEl.value.scrollHeight})}
function connect(){if(!enabled||!wsEnabled||!open.value||ws.value)return; try{ws.value=new WebSocket(WS_URL);ws.value.onopen=()=>{status.value='connected';addLog({level:'success',message:'Debug Console connected',source:'WebSocket'})};ws.value.onmessage=e=>{try{const d=JSON.parse(e.data);addLog({level:d.level||'info',message:d.message||'',source:'Django',payload:d})}catch{addLog({level:'info',message:e.data,source:'Django'})}};ws.value.onerror=()=>{status.value='error'};ws.value.onclose=()=>{status.value='closed';ws.value=null}}catch{status.value='error'}}
function disconnect(){ws.value?.close();ws.value=null;status.value='closed'}
function toggle(){open.value=!open.value;localStorage.setItem('debug_console_open',String(open.value)); if(open.value)connect();else disconnect()}
function onApi(e){const d=e.detail||{};addLog({level:d.phase==='error'?'error':d.phase==='response'?'success':'info',source:'API',message:`${d.method||''} ${d.url||''}`,payload:d})}
async function copyConsole(){const text=logs.value.map(x=>`[${x.time}] ${x.source||'APP'} ${x.level}: ${x.message}${x.payload?`\n${JSON.stringify(x.payload,null,2)}`:''}`).join('\n'); await navigator.clipboard?.writeText(text)}
onMounted(()=>{open.value=localStorage.getItem('debug_console_open')==='true';window.addEventListener('so-iam-api-log',onApi);if(open.value)connect()}); onBeforeUnmount(()=>{window.removeEventListener('so-iam-api-log',onApi);disconnect()})
</script>
<template><div v-if="enabled" class="debug-wrap"><button class="debug-toggle" @click="toggle"><i class="pi pi-terminal"/> Debug</button><section v-if="open" class="console" :class="{minimized}"><header><strong>Live Debug Console</strong><span>{{status}}</span><div><button @click="copyConsole">Copy</button><button @click="logs=[]">Clear</button><button @click="minimized=!minimized">{{minimized?'▲':'▼'}}</button><button @click="toggle">×</button></div></header><div v-if="!minimized" ref="consoleEl" class="body"><div v-if="!logs.length">Waiting for Django/API logs...</div><div v-for="log in logs" :key="log.id" class="line"><span>{{log.time}}</span><b>{{log.level}}</b><small>{{log.source}}</small><span>{{log.message}}</span><details v-if="log.payload"><summary>details</summary><pre>{{JSON.stringify(log.payload,null,2)}}</pre></details></div></div></section></div></template>
<style scoped>.debug-wrap{position:fixed;left:18px;bottom:18px;z-index:99999}.debug-toggle{background:#111827;color:#e5e7eb;border:1px solid #334155;border-radius:9px;padding:9px 12px;box-shadow:0 8px 30px #0005}.console{position:fixed;left:18px;right:18px;bottom:62px;height:360px;background:#07111f;border:1px solid #334155;border-radius:12px;color:#dbeafe;overflow:hidden;box-shadow:0 15px 50px #0008}.console.minimized{height:auto}.console header{display:flex;align-items:center;gap:12px;padding:10px 14px;border-bottom:1px solid #26364d}.console header span{color:#60a5fa;font-size:12px}.console header div{margin-left:auto;display:flex;gap:5px}.console button{background:#1f2937;color:#e5e7eb;border:0;border-radius:6px;padding:5px 8px}.body{height:calc(100% - 44px);overflow:auto;padding:10px;font:12px/1.6 monospace}.line{display:grid;grid-template-columns:85px 55px 65px minmax(200px,1fr) auto;gap:8px;border-bottom:1px solid #132238;padding:3px 0;align-items:start}.line span:first-child{color:#64748b}.line b{color:#93c5fd}.line small{color:#a5b4fc}.line pre{white-space:pre-wrap;max-width:65vw}.line details{grid-column:4/6}@media(max-width:700px){.console{left:8px;right:8px}.line{grid-template-columns:70px 50px 55px 1fr}.line details{grid-column:1/-1}}
</style> -->

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, nextTick } from 'vue'

// --- States & Configuration ---
const open = ref(false)
const minimized = ref(false)
const paused = ref(false)
const autoScroll = ref(true)
const searchQuery = ref('')
const activeFilter = ref('all') // 'all' | 'error' | 'warn' | 'network' | 'pinia'

const logs = ref([])
const status = ref('closed')
const ws = ref(null)
const frontendConsoleEl = ref(null)
const backendConsoleEl = ref(null)
const toastMessage = ref('')
const showToastFlag = ref(false)
let toastTimer = null

const enabled = true
const wsEnabled = import.meta.env.VITE_DEBUG_CONSOLE === 'true'
const WS_URL = import.meta.env.VITE_DEBUG_WS_URL || 'ws://127.0.0.1:8000/ws/debug/'

// --- Toast Notification Helper ---
function showToast(msg) {
  toastMessage.value = msg
  showToastFlag.value = true
  if (toastTimer) clearTimeout(toastTimer)
  toastTimer = setTimeout(() => {
    showToastFlag.value = false
  }, 2400)
}

// --- Clipboard Copy Helper ---
async function copyToClipboard(text, successMsg = 'تم النسخ إلى الحافظة بنجاح') {
  try {
    await navigator.clipboard?.writeText(text)
    showToast(successMsg)
  } catch {
    showToast('فشل النسخ')
  }
}

// --- Add Log Entry ---
const addLog = (entry) => {
  if (paused.value) return
  const newEntry = {
    id: Date.now() + Math.random(),
    time:
      entry.time ||
      new Date().toLocaleTimeString('ar-EG', { hour12: false, fractionalSecondDigits: 3 }),
    level: (entry.level || 'info').toLowerCase(),
    source: (entry.source || 'APP').toUpperCase(),
    message: entry.message || '',
    payload: entry.payload || null,
    isBackend: entry.source === 'Django' || entry.source === 'API' || entry.source === 'SQL',
  }

  logs.value = [...logs.value, newEntry].slice(-500)

  if (autoScroll.value) {
    nextTick(() => {
      if (frontendConsoleEl.value)
        frontendConsoleEl.value.scrollTop = frontendConsoleEl.value.scrollHeight
      if (backendConsoleEl.value)
        backendConsoleEl.value.scrollTop = backendConsoleEl.value.scrollHeight
    })
  }
}

// --- WebSocket Connection ---
function connect() {
  if (!enabled || !wsEnabled || !open.value || ws.value) return
  try {
    ws.value = new WebSocket(WS_URL)
    ws.value.onopen = () => {
      status.value = 'connected'
      addLog({
        level: 'success',
        message: 'Debug Console connected to Django Kernel',
        source: 'WebSocket',
      })
    }
    ws.value.onmessage = (e) => {
      try {
        const d = JSON.parse(e.data)
        addLog({
          level: d.level || 'info',
          message: d.message || '',
          source: d.source || 'Django',
          payload: d,
        })
      } catch {
        addLog({ level: 'info', message: e.data, source: 'Django' })
      }
    }
    ws.value.onerror = () => {
      status.value = 'error'
    }
    ws.value.onclose = () => {
      status.value = 'closed'
      ws.value = null
    }
  } catch {
    status.value = 'error'
  }
}

function disconnect() {
  ws.value?.close()
  ws.value = null
  status.value = 'closed'
}

function toggle() {
  open.value = !open.value
  localStorage.setItem('debug_console_open', String(open.value))
  if (open.value) connect()
  else disconnect()
}

// --- API Log Event Listener ---
function onApi(e) {
  const d = e.detail || {}
  addLog({
    level: d.phase === 'error' ? 'error' : d.phase === 'response' ? 'success' : 'info',
    source: 'API',
    message: `${d.method || ''} ${d.url || ''}`.trim(),
    payload: d,
  })
}

// --- Actions & Controls ---
function clearLogs() {
  logs.value = []
  showToast('تم تفريغ لوحة التصحيح بنجاح')
}

function copyAllConsole() {
  const text = logs.value
    .map(
      (x) =>
        `[${x.time}] [${x.source}] [${x.level.toUpperCase()}]: ${x.message}${x.payload ? `\nPayload: ${JSON.stringify(x.payload, null, 2)}` : ''}`,
    )
    .join('\n\n')
  copyToClipboard(text, 'تم نسخ كافة السجلات الحية بنجاح')
}

// --- Computed Filtered Logs ---
const filteredLogs = computed(() => {
  return logs.value.filter((log) => {
    if (searchQuery.value) {
      const q = searchQuery.value.toLowerCase()
      const matchText =
        `${log.message} ${log.source} ${JSON.stringify(log.payload || '')}`.toLowerCase()
      if (!matchText.includes(q)) return false
    }
    if (activeFilter.value === 'error' && log.level !== 'error') return false
    if (activeFilter.value === 'warn' && log.level !== 'warn' && log.level !== 'warning')
      return false
    if (activeFilter.value === 'network' && log.source !== 'API' && log.source !== 'WEBSOCKET')
      return false
    if (
      activeFilter.value === 'pinia' &&
      !log.message.includes('Pinia') &&
      !log.source.includes('PINIA')
    )
      return false
    return true
  })
})

const clientLogs = computed(() => filteredLogs.value.filter((l) => !l.isBackend))
const backendLogs = computed(() => filteredLogs.value.filter((l) => l.isBackend))

// Lifecycle Hooks
onMounted(() => {
  open.value = localStorage.getItem('debug_console_open') === 'true'
  window.addEventListener('so-iam-api-log', onApi)
  if (open.value) connect()
})

onBeforeUnmount(() => {
  window.removeEventListener('so-iam-api-log', onApi)
  disconnect()
})
</script>

<template>
  <div v-if="enabled" class="fixed left-5 bottom-5 z-[99999] font-body-md">
    <!-- PrimeVue Button للزر العائم الرئيسي -->
    <Button
      class="p-button-secondary flex items-center gap-2 bg-surface-container-lowest text-on-surface border border-outline-variant rounded-xl px-4 py-2.5 shadow-2xl hover:bg-surface-container-high transition-all"
      @click="toggle"
    >
      <span class="font-label-md text-label-md"> Debug Console</span>
      <span
        class="w-2 h-2 rounded-full"
        :class="status === 'connected' ? 'bg-tertiary animate-pulse' : 'bg-error'"
      ></span>
    </Button>

    <!-- Main Command Center Overlay / Drawer -->
    <div
      v-if="open"
      class="fixed inset-x-4 bottom-16 md:inset-x-8 md:bottom-20 max-w-[96vw] mx-auto h-[82vh] max-h-[760px] bg-surface-container-lowest border border-outline-variant rounded-2xl shadow-[0_25px_60px_rgba(0,0,0,0.8)] flex flex-col overflow-hidden z-[100000] backdrop-blur-2xl transition-all"
      :class="{ 'h-14 overflow-hidden': minimized }"
    >
      <!-- Top Header Bar -->
      <div
        class="px-4 py-3 bg-surface-container-low border-b border-outline-variant flex flex-wrap items-center justify-between gap-3"
      >
        <div class="flex items-center gap-3">
          <div
            class="w-8 h-8 rounded-lg bg-surface-container flex items-center justify-center text-primary shadow-sm"
          >
            <span class="material-symbols-outlined text-[18px]">terminal</span>
          </div>
          <div>
            <div class="flex items-center gap-2">
              <span
                class="font-headline-sm text-headline-sm text-on-surface font-semibold tracking-tight"
                >Live Debug Console</span
              >
              <span
                class="px-1.5 py-0.5 rounded bg-surface-container-high text-primary font-code-sm text-[10px] uppercase font-semibold"
                >&lt;LiveDebugConsole.vue&gt;</span
              >
            </div>
            <span class="font-body-sm text-[11px] text-outline"
              >Real-time bidirectional reactive telemetry & trace inspector (Socket:
              {{ status }})</span
            >
          </div>
        </div>

        <!-- Toolbar Actions with PrimeVue Buttons -->
        <div class="flex flex-wrap items-center gap-2">
          <Button
            class="p-button-sm p-button-text flex items-center gap-1.5 text-on-surface-variant hover:text-on-surface"
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
            class="p-button-sm p-button-text flex items-center gap-1.5 text-on-surface-variant hover:text-on-surface"
            @click="paused = !paused"
          >
            <span class="material-symbols-outlined text-[16px]">{{
              paused ? 'play_arrow' : 'pause'
            }}</span>
            <span class="text-label-sm">{{ paused ? 'Resume' : 'Pause' }}</span>
          </Button>

          <Button
            class="p-button-sm p-button-text flex items-center gap-1.5 text-on-surface-variant hover:text-error"
            @click="clearLogs"
          >
            <span class="material-symbols-outlined text-[16px]">block</span>
            <span class="text-label-sm">Clear</span>
          </Button>

          <Button
            class="p-button-sm bg-primary text-on-primary font-medium shadow-sm hover:bg-primary-container flex items-center gap-1.5"
            @click="copyAllConsole"
          >
            <span class="material-symbols-outlined text-[16px]">content_copy</span>
            <span class="text-label-sm">Copy All</span>
          </Button>

          <div class="flex items-center gap-1 pl-2 border-l border-outline-variant/50">
            <Button
              class="p-button-sm p-button-text text-outline hover:text-on-surface"
              @click="minimized = !minimized"
            >
              <span class="material-symbols-outlined text-[18px]">{{
                minimized ? 'open_in_full' : 'minimize'
              }}</span>
            </Button>
            <Button class="p-button-sm p-button-text text-outline hover:text-error" @click="toggle">
              <span class="material-symbols-outlined text-[18px]">close</span>
            </Button>
          </div>
        </div>
      </div>

      <!-- Sub-Toolbar: Filters & PrimeVue InputText -->
      <div
        v-if="!minimized"
        class="px-4 py-2.5 bg-surface-container border-b border-outline-variant/60 flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3"
      >
        <div class="flex items-center gap-1 overflow-x-auto py-0.5">
          <Button
            class="p-button-sm whitespace-nowrap"
            :class="
              activeFilter === 'all'
                ? 'p-button-primary font-semibold'
                : 'p-button-text text-on-surface-variant'
            "
            @click="activeFilter = 'all'"
            :label="`All Events (${logs.length})`"
          />
          <Button
            class="p-button-sm whitespace-nowrap"
            :class="
              activeFilter === 'error'
                ? 'bg-error text-on-error font-semibold'
                : 'p-button-text text-on-surface-variant'
            "
            @click="activeFilter = 'error'"
            label="Errors"
          />
          <Button
            class="p-button-sm whitespace-nowrap"
            :class="
              activeFilter === 'warn'
                ? 'bg-secondary-container text-on-secondary-container font-semibold'
                : 'p-button-text text-on-surface-variant'
            "
            @click="activeFilter = 'warn'"
            label="Warnings"
          />
          <Button
            class="p-button-sm whitespace-nowrap"
            :class="
              activeFilter === 'network'
                ? 'p-button-primary font-semibold'
                : 'p-button-text text-on-surface-variant'
            "
            @click="activeFilter = 'network'"
            label="Network & API"
          />
          <Button
            class="p-button-sm whitespace-nowrap"
            :class="
              activeFilter === 'pinia'
                ? 'bg-tertiary-container text-on-tertiary-container font-semibold'
                : 'p-button-text text-on-surface-variant'
            "
            @click="activeFilter = 'pinia'"
            label="Pinia / State"
          />
        </div>

        <!-- PrimeVue InputText Search Field -->
        <div class="relative flex-1 md:max-w-xs">
          <span class="p-input-icon-left w-full">
            <span
              class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-[16px] text-outline"
              >search</span
            >
            <InputText
              v-model="searchQuery"
              class="w-full bg-surface-container-low border border-outline-variant/40 text-on-surface text-code-sm pl-9 py-1.5 rounded-lg"
              placeholder="Filter logs or search payload..."
            />
          </span>
        </div>
      </div>

      <!-- Split Screen Content Body (Left: Frontend / Right: Backend) -->
      <div
        v-if="!minimized"
        class="grid grid-cols-1 lg:grid-cols-2 flex-1 overflow-hidden divide-y lg:divide-y-0 lg:divide-x divide-outline-variant/50 bg-surface"
      >
        <!-- LEFT PANEL: CLIENT / FRONTEND RUNTIME -->
        <section class="flex flex-col h-full overflow-hidden bg-surface-container-lowest/40">
          <div
            class="px-4 py-2 bg-surface-container-low/80 border-b border-outline-variant/40 flex items-center justify-between"
          >
            <div class="flex items-center gap-2">
              <span class="material-symbols-outlined text-tertiary text-[16px]">devices</span>
              <span class="font-headline-sm text-label-md text-on-surface font-semibold"
                >CLIENT RUNTIME (Frontend)</span
              >
            </div>
            <span class="font-code-sm text-[10px] text-outline"
              >{{ clientLogs.length }} events</span
            >
          </div>

          <div
            ref="frontendConsoleEl"
            class="flex-1 overflow-y-auto p-3 font-code-sm text-code-sm space-y-2 select-text"
          >
            <div
              v-if="!clientLogs.length"
              class="h-full flex items-center justify-center text-outline italic text-xs"
            >
              Waiting for frontend client events...
            </div>

            <div
              v-for="log in clientLogs"
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
                    {{ log.level }}
                  </span>
                  <span class="text-on-surface font-medium truncate">{{ log.message }}</span>
                </div>

                <!-- PrimeVue Button للنسخ الفردي -->
                <Button
                  class="p-button-sm p-button-text p-button-rounded opacity-0 group-hover:opacity-100 transition-opacity text-outline hover:text-on-surface"
                  @click="
                    copyToClipboard(
                      log.payload ? JSON.stringify(log.payload, null, 2) : log.message,
                      'تم نسخ محتوى السجل بنجاح',
                    )
                  "
                  title="نسخ عنصر البيانات"
                >
                  <span class="material-symbols-outlined text-[14px]">content_copy</span>
                </Button>
              </div>

              <div
                v-if="log.payload"
                class="mt-1 pl-3 bg-surface-container-lowest rounded p-2 overflow-x-auto border border-outline-variant/20"
              >
                <pre
                  class="text-[11px] font-code-sm leading-relaxed text-on-surface-variant whitespace-pre-wrap"
                  >{{ JSON.stringify(log.payload, null, 2) }}</pre>
              </div>
            </div>
          </div>
        </section>

        <!-- RIGHT PANEL: BACKEND ENGINE & APIS -->
        <section class="flex flex-col h-full overflow-hidden bg-surface-container-lowest/40">
          <div
            class="px-4 py-2 bg-surface-container-low/80 border-b border-outline-variant/40 flex items-center justify-between"
          >
            <div class="flex items-center gap-2">
              <span class="material-symbols-outlined text-primary text-[16px]">dns</span>
              <span class="font-headline-sm text-label-md text-on-surface font-semibold"
                >BACKEND ENGINE & APIS (Django)</span
              >
            </div>
            <span class="font-code-sm text-[10px] text-outline"
              >{{ backendLogs.length }} events</span
            >
          </div>

          <div
            ref="backendConsoleEl"
            class="flex-1 overflow-y-auto p-3 font-code-sm text-code-sm space-y-2 select-text"
          >
            <div
              v-if="!backendLogs.length"
              class="h-full flex items-center justify-center text-outline italic text-xs"
            >
              Waiting for Django backend & API logs...
            </div>

            <div
              v-for="log in backendLogs"
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
                      'bg-tertiary-container/30 text-tertiary':
                        log.level === 'success' || log.level === 'info',
                      'bg-error-container text-error': log.level === 'error',
                      'bg-secondary-container/30 text-secondary':
                        log.level === 'warn' || log.level === 'warning',
                    }"
                  >
                    {{ log.source }}
                  </span>
                  <span class="text-on-surface font-medium truncate">{{ log.message }}</span>
                </div>

                <!-- PrimeVue Button للنسخ الفردي -->
                <Button
                  class="p-button-sm p-button-text p-button-rounded opacity-0 group-hover:opacity-100 transition-opacity text-outline hover:text-on-surface"
                  @click="
                    copyToClipboard(
                      log.payload ? JSON.stringify(log.payload, null, 2) : log.message,
                      'تم نسخ محتوى سجل الباك إند بنجاح',
                    )
                  "
                  title="نسخ بيانات الباك إند"
                >
                  <span class="material-symbols-outlined text-[14px]">content_copy</span>
                </Button>
              </div>

              <div
                v-if="log.payload"
                class="mt-1 pl-3 bg-surface-container-lowest rounded p-2 overflow-x-auto border border-outline-variant/20"
              >
                <pre
                  class="text-[11px] font-code-sm leading-relaxed text-on-surface-variant whitespace-pre-wrap"
                  >{{ JSON.stringify(log.payload, null, 2) }}</pre>
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
        <div class="flex items-center gap-4">
          <div class="flex items-center gap-1.5">
            <span
              class="w-2 h-2 rounded-full"
              :class="status === 'connected' ? 'bg-tertiary' : 'bg-error'"
            ></span>
            <span
              >STATUS: <strong class="text-on-surface uppercase">{{ status }}</strong></span
            >
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

    <!-- Floating Toast Notification Popup -->
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
</template>


