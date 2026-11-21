<script setup>
import { ref, onMounted } from 'vue'

// States
const activeTab = ref('vue')
const isInspectMode = ref(true)
const currentTarget = ref('HeaderBar Component')
const toastMessage = ref('')
const showToast = ref(false)

// Code Snippets for Inspector Tabs (تم إصلاح التعليقات والنصوص البرمجية لتجنب تداخل الـ SFC Parser)
const codeSnippets = {
  vue: `// src/components/HeaderBar.vue
<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const username = ref('Eng. Ahmed')
const systemStatus = ref('Operational')

function refreshTelemetry() {
  console.log('Fetching live DRF telemetry...')
}
<\/script>

<template>
  <div class="p-5 bg-[#101728] border border-brand-border rounded-2xl">
    <h1>Welcome back, {{ username }} 👋</h1>
    <span class="badge-operational">{{ systemStatus }}</span>
  </div>
</template>`,

  django: `# backend/api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class TelemetryStreamView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = {
            "cluster_load": 64.5,
            "active_sockets": 3420,
            "sla_rate": 99.94
        }
        return Response({"status": "success", "data": data})`,

  ws: `// channels/consumers.py & frontend useWebSocket
import { useWebSocket } from '@vueuse/core'

const { status, data, send } = useWebSocket('wss://api.codex.internal/v1/telemetry/ws', {
  autoReconnect: {
    retries: 5,
    delay: 1000,
  },
  onMessage(ws, event) {
    const frame = JSON.parse(event.data)
    console.log('Incoming telemetry frame:', frame)
  }
})`,

  schema: `// serializers.py / Zod DTO Schema
import { z } from 'zod'

export const TelemetryFrameSchema = z.object({
  jobId: z.string().regex(/^#REQ-\\d+$/),
  processName: z.string(),
  latencyMs: z.number().min(0),
  status: z.enum(['SUCCESS', 'RUNNING', 'FAILED'])
})

export type TelemetryFrameDTO = z.infer<typeof TelemetryFrameSchema>`,
}

const filePathDisplayMap = {
  vue: 'src/components/HeaderBar.vue',
  django: 'backend/api/views.py',
  ws: 'src/composables/useLiveTelemetry.ts',
  schema: 'src/schemas/telemetry.schema.ts',
}

const activeComponentTagMap = {
  vue: '<HeaderBar />',
  django: '<TelemetryStreamView />',
  ws: '<LiveWebSocketTelemetry />',
  schema: '<TelemetryFrameDTO />',
}

// Actions & Handlers
function switchCodeTab(tab) {
  activeTab.value = tab
}

function toggleInspectMode() {
  isInspectMode.value = !isInspectMode.value
  triggerActionLog(
    isInspectMode.value ? 'Inspect Element Mode Enabled' : 'Inspect Element Mode Disabled',
  )
}

function selectComponent(componentName) {
  const mapNames = {
    header: 'HeaderBar Component',
    websocket: 'LiveWebSocketTelemetry Component',
    kpi: 'KpiGridWidget Component',
    table: 'DataTable & Telemetry Pipeline',
    routes: 'RouterGateway Component',
  }
  currentTarget.value = mapNames[componentName] || componentName
  triggerActionLog(`Selected node: <${componentName} />`)
}

function triggerActionLog(msg) {
  toastMessage.value = msg
  showToast.value = true
  setTimeout(() => {
    showToast.value = false
  }, 3000)
}

function copyCurrentCode() {
  const code = codeSnippets[activeTab.value]
  navigator.clipboard.writeText(code)
  triggerActionLog('Code snippet copied to clipboard!')
}

onMounted(() => {
  if (window.lucide) {
    window.lucide.createIcons()
  }
})
</script>

<template>
  <div
    class="bg-[#0a0d14] text-slate-200 font-sans antialiased h-screen flex flex-col overflow-hidden select-none"
  >
    <!-- Top Global Application Bar -->
    <header
      class="h-14 border-b border-brand-border bg-[#0d121f] px-4 flex items-center justify-between z-20 shrink-0"
    >
      <div class="flex items-center gap-3">
        <div class="flex items-center gap-2">
          <div
            class="w-8 h-8 rounded-lg bg-gradient-to-tr from-indigo-600 via-indigo-500 to-cyan-400 flex items-center justify-center shadow-lg shadow-indigo-600/30"
          >
            <i class="w-4 h-4 text-white" data-lucide="layers"></i>
          </div>
          <div>
            <span
              class="font-extrabold text-sm tracking-tight text-white flex items-center gap-1.5"
            >
              DevStudio
              <span
                class="text-[10px] uppercase font-mono px-1.5 py-0.5 rounded bg-indigo-950 text-indigo-400 border border-indigo-800/60"
                >Inspector</span
              >
            </span>
          </div>
        </div>
      </div>

      <!-- Center Mode Switch -->
      <div
        class="flex items-center gap-1.5 bg-[#0a0d14] border border-brand-border p-1 rounded-lg text-xs"
      >
        <button
          class="px-2.5 py-1 rounded-md flex items-center gap-1.5 transition-all font-medium"
          :class="
            isInspectMode
              ? 'bg-indigo-600/20 text-indigo-300 border border-indigo-500/40'
              : 'text-slate-400 hover:text-white'
          "
          @click="toggleInspectMode"
        >
          <i class="w-3.5 h-3.5 text-indigo-400 animate-pulse" data-lucide="crosshair"></i>
          <span>Inspect Element Mode</span>
        </button>
        <div class="h-4 w-px bg-brand-border"></div>
        <div class="px-2 text-slate-400 text-[11px] font-mono flex items-center gap-1">
          Target: <span class="text-indigo-300 font-semibold">{{ currentTarget }}</span>
        </div>
      </div>

      <!-- Right Controls -->
      <div class="flex items-center gap-2.5">
        <button
          class="p-1.5 rounded-lg border border-brand-border text-slate-400 hover:text-white hover:bg-brand-surface text-xs flex items-center gap-1 transition-all"
          @click="triggerActionLog('Hot reload executed')"
          title="Reload Canvas"
        >
          <i class="w-4 h-4" data-lucide="rotate-cw"></i>
        </button>
        <a
          class="px-3 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold flex items-center gap-1.5 shadow-md shadow-indigo-600/20 transition-all"
          href="http://localhost:5173/dashboard"
          target="_blank"
        >
          <span>Launch App</span>
          <i class="w-3.5 h-3.5" data-lucide="external-link"></i>
        </a>
      </div>
    </header>

    <!-- Main Workspace: Split Screen Layout -->
    <main class="flex-1 flex overflow-hidden">
      <!-- LEFT SIDE: Dual/Multi-Tab Code Inspector -->
      <section class="w-1/2 flex flex-col border-r border-brand-border bg-[#0a0d14] relative">
        <div
          class="h-11 border-b border-brand-border bg-[#0e1321] px-3 flex items-center justify-between shrink-0"
        >
          <div class="flex items-center gap-1 overflow-x-auto">
            <button
              class="px-3 py-1.5 rounded-md text-xs font-medium flex items-center gap-2 transition-all whitespace-nowrap"
              :class="
                activeTab === 'vue'
                  ? 'bg-[#172036] text-white border border-brand-borderLight shadow-sm'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-[#141b2d]'
              "
              @click="switchCodeTab('vue')"
            >
              <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
              <span>Frontend (Vue 3)</span>
            </button>
            <button
              class="px-3 py-1.5 rounded-md text-xs font-medium flex items-center gap-2 transition-all whitespace-nowrap"
              :class="
                activeTab === 'django'
                  ? 'bg-[#172036] text-white border border-brand-borderLight shadow-sm'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-[#141b2d]'
              "
              @click="switchCodeTab('django')"
            >
              <span class="w-2 h-2 rounded-full bg-cyan-400"></span>
              <span>Backend (Django DRF)</span>
            </button>
            <button
              class="px-3 py-1.5 rounded-md text-xs font-medium flex items-center gap-2 transition-all whitespace-nowrap"
              :class="
                activeTab === 'ws'
                  ? 'bg-[#172036] text-white border border-brand-borderLight shadow-sm'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-[#141b2d]'
              "
              @click="switchCodeTab('ws')"
            >
              <span class="w-2 h-2 rounded-full bg-amber-400 animate-ping"></span>
              <span>WebSocket</span>
            </button>
            <button
              class="px-2.5 py-1.5 rounded-md text-xs font-medium flex items-center gap-1.5 transition-all whitespace-nowrap"
              :class="
                activeTab === 'schema'
                  ? 'bg-[#172036] text-white border border-brand-borderLight shadow-sm'
                  : 'text-slate-500 hover:text-slate-300'
              "
              @click="switchCodeTab('schema')"
            >
              <span>DTO Schema</span>
            </button>
          </div>
          <div class="flex items-center gap-2 pl-2">
            <span class="text-[11px] font-mono text-slate-400 hidden lg:inline-block">{{
              filePathDisplayMap[activeTab]
            }}</span>
            <button
              class="p-1.5 rounded bg-brand-surface border border-brand-border hover:border-slate-500 text-slate-400 hover:text-white transition-all text-xs"
              @click="copyCurrentCode"
              title="Copy code snippet"
            >
              <i class="w-3.5 h-3.5" data-lucide="copy"></i>
            </button>
          </div>
        </div>

        <!-- Code Viewer Content -->
        <div
          class="flex-1 overflow-auto p-4 font-mono text-[12.5px] leading-relaxed relative bg-[#0a0d14]"
        >
          <pre class="text-slate-300 m-0 p-0 font-mono whitespace-pre">{{
            codeSnippets[activeTab]
          }}</pre>
        </div>
      </section>

      <!-- RIGHT SIDE: Live Browser Preview -->
      <section class="w-1/2 flex flex-col bg-[#0f1422] relative overflow-hidden">
        <div class="flex-1 overflow-y-auto p-5 bg-[#0a0d14] text-slate-100 relative space-y-5">
          <!-- Toast Notification -->
          <div
            class="transition-all duration-300 fixed top-16 right-8 z-50 bg-indigo-950/90 border border-indigo-500/70 text-indigo-200 px-4 py-2.5 rounded-xl shadow-2xl backdrop-blur-md flex items-center gap-2.5 text-xs font-mono"
            :class="
              showToast
                ? 'opacity-100 translate-y-0'
                : 'opacity-0 -translate-y-2 pointer-events-none'
            "
          >
            <i class="w-4 h-4 text-indigo-400" data-lucide="zap"></i>
            <span>{{ toastMessage }}</span>
          </div>

          <!-- Header Component Node -->
          <div
            class="component-node bg-[#101728] border border-brand-border rounded-2xl p-5 shadow-lg relative group cursor-pointer"
            :class="{ 'active-inspect': isInspectMode }"
            @click="selectComponent('header')"
          >
            <div
              class="absolute -top-2.5 right-4 bg-indigo-600 text-white text-[10px] font-mono px-2 py-0.5 rounded-full uppercase tracking-wider font-bold shadow"
            >
              &lt;HeaderBar /&gt;
            </div>
            <h1 class="text-xl font-bold text-white tracking-tight flex items-center gap-2">
              <span>Welcome back, Eng. Ahmed</span>
              <span class="text-lg">👋</span>
            </h1>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<style scoped>
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
::-webkit-scrollbar-track {
  background: #0a0d14;
}
::-webkit-scrollbar-thumb {
  background: #252f48;
  border-radius: 4px;
}
.component-node {
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}
.component-node:hover {
  outline: 2px solid #6366f1;
  outline-offset: 2px;
  cursor: pointer;
}
.component-node.active-inspect {
  outline: 2px solid #818cf8 !important;
  outline-offset: 2px;
  box-shadow: 0 0 20px -3px rgba(99, 102, 241, 0.45);
}
</style>
