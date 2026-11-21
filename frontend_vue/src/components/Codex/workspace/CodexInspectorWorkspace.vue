<script setup>
import { computed, onBeforeUnmount, ref, watch } from 'vue'

const props = defineProps({
  features: { type: Array, default: () => [] },
  files: { type: Array, default: () => [] },
  apis: { type: Array, default: () => [] },
  routes: { type: Array, default: () => [] },
  loading: Boolean,
})
const emit = defineEmits(['openFile', 'askAI', 'scan'])

const activeApp = ref(null)
const activeRoute = ref('')
const inspectEnabled = ref(false)
const viewport = ref('desktop')
const selectedElement = ref(null)
const resourcePaths = ref([])
const previewError = ref('')
const frame = ref(null)
let detachInspector = null

const appFeatures = computed(() => [...props.features].sort((a, b) => (a.name || '').localeCompare(b.name || '')))
const activeRoutes = computed(() => {
  if (!activeApp.value) return []
  const slug = String(activeApp.value.app_label || activeApp.value.name || '').toLowerCase().replace(/[^a-z0-9]+/g, '')
  return props.routes.filter((route) => {
    const routeText = `${route.name || ''} ${route.path || ''}`.toLowerCase().replace(/[^a-z0-9]+/g, '')
    return slug && routeText.includes(slug)
  })
})
const currentRoute = computed(() => props.routes.find((route) => route.path === activeRoute.value) || null)
const matchedFile = computed(() => {
  const path = selectedElement.value?.sourcePath
  if (!path) return null
  const normalized = path.replaceAll('\\', '/').replace(/^.*?frontend_vue\//, 'frontend_vue/')
  return props.files.find((file) => file.path === normalized || normalized.endsWith(file.path)) || null
})
const relatedApis = computed(() => {
  const observed = resourcePaths.value
  return props.apis.filter((api) => observed.some((url) => {
    const path = url.split('?')[0].replace(/\/$/, '')
    const endpoint = String(api.path || '').replace(/\/$/, '')
    return endpoint && (path === endpoint || path.endsWith(endpoint) || endpoint.endsWith(path))
  }))
})

function chooseApp(app) {
  activeApp.value = app
  selectedElement.value = null
  resourcePaths.value = []
  previewError.value = ''
  const candidates = props.routes.filter((route) => {
    const slug = String(app.app_label || app.name || '').toLowerCase().replace(/[^a-z0-9]+/g, '')
    const routeText = `${route.name || ''} ${route.path || ''}`.toLowerCase().replace(/[^a-z0-9]+/g, '')
    return slug && routeText.includes(slug)
  })
  activeRoute.value = candidates[0]?.path || ''
}

function readElement(element, doc) {
  const chain = []
  let node = element
  let vueComponent = null
  let sourcePath = ''
  while (node && node !== doc.body && chain.length < 12) {
    const tag = node.tagName?.toLowerCase()
    if (tag) {
      chain.push({
        tag,
        id: node.id || '',
        classes: typeof node.className === 'string' ? node.className.trim().split(/\s+/).filter(Boolean).slice(0, 5) : [],
        text: (node.innerText || node.getAttribute?.('aria-label') || '').trim().slice(0, 100),
      })
    }
    const instance = node.__vueParentComponent
    if (!vueComponent && instance?.type) {
      vueComponent = instance.type.name || instance.type.__name || instance.type.__file?.split('/').pop() || ''
      sourcePath = instance.type.__file || ''
    }
    node = node.parentElement
  }
  const attributes = [...(element.attributes || [])].slice(0, 30).map((attr) => ({ name: attr.name, value: attr.value.slice(0, 240) }))
  return {
    tag: element.tagName?.toLowerCase() || 'unknown',
    text: (element.innerText || element.getAttribute?.('aria-label') || '').trim().slice(0, 500),
    id: element.id || '',
    classes: typeof element.className === 'string' ? element.className : '',
    attributes,
    hierarchy: chain,
    component: vueComponent || 'Component metadata not exposed by this build',
    sourcePath,
  }
}

function attachInspector() {
  detachInspector?.()
  const doc = frame.value?.contentDocument
  if (!doc) {
    previewError.value = 'The preview document is not accessible. Confirm that the preview is served from the same origin.'
    return
  }
  previewError.value = ''
  const previousOutline = new WeakMap()
  let hovered = null
  const onMove = (event) => {
    if (!inspectEnabled.value) return
    if (hovered && hovered !== event.target) hovered.style.outline = previousOutline.get(hovered) || ''
    hovered = event.target
    if (hovered && hovered !== doc.body && hovered !== doc.documentElement) {
      if (!previousOutline.has(hovered)) previousOutline.set(hovered, hovered.style.outline)
      hovered.style.outline = '2px solid #38bdf8'
      hovered.style.outlineOffset = '2px'
    }
  }
  const onClick = (event) => {
    if (!inspectEnabled.value) return
    event.preventDefault()
    event.stopPropagation()
    event.stopImmediatePropagation()
    const element = event.target
    if (hovered) hovered.style.outline = previousOutline.get(hovered) || ''
    selectedElement.value = readElement(element, doc)
    const paths = doc.defaultView.performance.getEntriesByType('resource').map((entry) => entry.name).filter((url) => /\/api\//i.test(url))
    resourcePaths.value = [...new Set(paths)].slice(-100)
  }
  const onLoad = () => {
    resourcePaths.value = [...new Set(doc.defaultView.performance.getEntriesByType('resource').map((entry) => entry.name).filter((url) => /\/api\//i.test(url)))].slice(-100)
  }
  doc.addEventListener('mousemove', onMove, true)
  doc.addEventListener('click', onClick, true)
  doc.defaultView.addEventListener('load', onLoad)
  onLoad()
  detachInspector = () => {
    doc.removeEventListener('mousemove', onMove, true)
    doc.removeEventListener('click', onClick, true)
    doc.defaultView.removeEventListener('load', onLoad)
    if (hovered) hovered.style.outline = previousOutline.get(hovered) || ''
  }
}

function onFrameLoad() {
  attachInspector()
}
function toggleInspect() {
  inspectEnabled.value = !inspectEnabled.value
  if (inspectEnabled.value) attachInspector()
  else detachInspector?.()
}
function openSource() {
  if (matchedFile.value) emit('openFile', matchedFile.value)
}
function askAboutSelection() {
  const element = selectedElement.value
  if (!element) return
  emit('askAI', `Explain this inspected frontend element using only discovered source relationships. Page: ${currentRoute.value?.path || 'unknown'}. Element: ${JSON.stringify(element)}. Related API endpoints: ${JSON.stringify(relatedApis.value)}. Clearly state unresolved mappings.`)
}
watch(activeRoute, () => {
  selectedElement.value = null
  resourcePaths.value = []
  previewError.value = ''
})
onBeforeUnmount(() => detachInspector?.())
</script>

<template>
  <section class="codex-inspector flex-1 min-w-0 min-h-0 flex flex-col bg-[#090d15] text-slate-200">
    <header class="flex flex-wrap items-center gap-3 px-4 py-3 border-b border-slate-800 bg-[#0d1320]">
      <div class="min-w-0 mr-auto">
        <div class="text-sm font-semibold">Project Intelligence · Live Inspector</div>
        <div class="text-[11px] text-slate-500">Application discovery and preview use the registered project data and actual Vue routes.</div>
      </div>
      <button class="px-3 py-1.5 rounded border border-slate-700 text-xs text-slate-300" @click="emit('scan')">Scan project</button>
      <button class="px-3 py-1.5 rounded border text-xs" :class="inspectEnabled ? 'border-sky-400 bg-sky-500/15 text-sky-200' : 'border-slate-700 text-slate-300'" @click="toggleInspect">
        {{ inspectEnabled ? 'Exit inspect mode' : 'Inspect page elements' }}
      </button>
      <button class="px-3 py-1.5 rounded border border-slate-700 text-xs text-slate-300" @click="frame?.contentWindow?.location.reload()">Refresh preview</button>
    </header>

    <div class="flex flex-1 min-h-0 overflow-hidden">
      <aside class="w-60 shrink-0 border-r border-slate-800 flex flex-col min-h-0 bg-[#0c111c]">
        <div class="px-3 py-3 border-b border-slate-800 flex justify-between items-center">
          <span class="text-[11px] font-semibold uppercase tracking-wider text-slate-400">Applications</span>
          <span class="text-[10px] text-slate-600">{{ appFeatures.length }}</span>
        </div>
        <div class="p-2 border-b border-slate-800 text-[10px] text-slate-500">Registry-backed application list</div>
        <div class="overflow-y-auto p-2 space-y-1">
          <button v-for="app in appFeatures" :key="app.id || app.key" class="w-full text-left px-2.5 py-2 rounded text-xs flex items-center gap-2" :class="activeApp?.id === app.id ? 'bg-sky-500/15 text-sky-200' : 'text-slate-400 hover:bg-slate-800/70'" @click="chooseApp(app)">
            <i class="pi pi-box text-[11px]" /> <span class="truncate">{{ app.name }}</span>
            <span class="ml-auto text-[9px] text-slate-600">{{ app.app_label }}</span>
          </button>
          <div v-if="!loading && !appFeatures.length" class="p-3 text-xs text-slate-500">No application registry data. Run a project scan first.</div>
        </div>
      </aside>

      <div class="flex-1 min-w-0 min-h-0 flex flex-col">
        <div class="flex flex-wrap items-center gap-2 px-3 py-2 border-b border-slate-800 bg-[#0c111c]">
          <span class="text-[10px] uppercase tracking-wider text-slate-500">Preview</span>
          <span class="text-xs text-slate-300">{{ activeApp?.name || 'Select an application' }}</span>
          <select v-model="activeRoute" class="ml-auto max-w-[260px] bg-[#111a29] border border-slate-700 rounded px-2 py-1.5 text-xs text-slate-300">
            <option value="">No discovered route</option>
            <option v-for="route in activeRoutes" :key="route.path" :value="route.path">{{ route.name || route.path }} · {{ route.path }}</option>
          </select>
          <div class="flex rounded border border-slate-700 overflow-hidden">
            <button v-for="mode in ['desktop','mobile']" :key="mode" class="px-2 py-1 text-[10px] capitalize" :class="viewport === mode ? 'bg-slate-700 text-white' : 'text-slate-400'" @click="viewport = mode">{{ mode }}</button>
          </div>
        </div>
        <div class="flex-1 min-h-0 overflow-auto flex justify-center items-stretch p-3 bg-[#080b12]">
          <div v-if="!activeRoute" class="m-auto max-w-md text-center text-xs text-slate-500 leading-6">
            Select an application with a route discovered from the active Vue Router configuration. If no matching route is found, no preview is fabricated.
          </div>
          <iframe v-else ref="frame" :key="activeRoute" :src="activeRoute" :title="`SO_IAM_OS preview ${activeRoute}`" class="bg-white border border-slate-700 rounded" :class="viewport === 'mobile' ? 'w-[390px] max-w-full' : 'w-full'" @load="onFrameLoad" />
        </div>
        <div v-if="previewError" class="px-3 py-2 text-[11px] text-amber-300 border-t border-amber-900/60">{{ previewError }}</div>
        <div class="px-3 py-2 border-t border-slate-800 text-[10px] text-slate-500 flex flex-wrap gap-3">
          <span>Route: {{ activeRoute || '—' }}</span><span>Observed API requests: {{ resourcePaths.length }}</span><span v-if="inspectEnabled" class="text-sky-300">Inspection mode active · clicks are captured inside preview</span>
        </div>
      </div>

      <aside class="w-[310px] shrink-0 border-l border-slate-800 bg-[#0c111c] overflow-y-auto">
        <div class="px-3 py-3 border-b border-slate-800 text-[11px] font-semibold uppercase tracking-wider text-slate-400">Element Inspector</div>
        <div v-if="!selectedElement" class="p-4 text-xs text-slate-500 leading-6">Enable inspection, then click an element in the preview. Component source metadata is shown only when exposed by the running Vue build.</div>
        <template v-else>
          <div class="p-3 border-b border-slate-800 space-y-2">
            <div class="text-sm font-semibold text-slate-100">{{ selectedElement.component }}</div>
            <div class="text-[11px] text-slate-400">{{ selectedElement.tag }} <span v-if="selectedElement.id">#{{ selectedElement.id }}</span></div>
            <div class="text-[11px] text-slate-500 break-words">{{ selectedElement.text || 'No visible text' }}</div>
            <div class="text-[10px] text-slate-500 break-all">Source: {{ selectedElement.sourcePath || 'Not exposed by current build' }}</div>
            <button v-if="matchedFile" class="text-[11px] text-sky-300 hover:text-sky-200" @click="openSource">Open source in editor →</button>
            <button class="block text-[11px] text-violet-300 hover:text-violet-200" @click="askAboutSelection">Ask Codex about this element →</button>
          </div>
          <div class="p-3 border-b border-slate-800">
            <div class="text-[10px] uppercase tracking-wider text-slate-500 mb-2">DOM hierarchy</div>
            <div v-for="(node, index) in selectedElement.hierarchy" :key="index" class="font-mono text-[10px] py-1 pl-2 border-l border-slate-700" :style="{ marginLeft: `${index * 7}px` }">
              <span class="text-sky-300">{{ node.tag }}</span><span v-if="node.id" class="text-amber-300">#{{ node.id }}</span><span v-if="node.classes.length" class="text-slate-500">.{{ node.classes.join('.') }}</span>
            </div>
          </div>
          <div class="p-3 border-b border-slate-800">
            <div class="text-[10px] uppercase tracking-wider text-slate-500 mb-2">Attributes</div>
            <div v-for="attr in selectedElement.attributes" :key="attr.name" class="grid grid-cols-[85px_1fr] gap-2 py-1 text-[10px]"><span class="text-violet-300">{{ attr.name }}</span><span class="text-slate-400 break-all">{{ attr.value }}</span></div>
          </div>
          <div class="p-3">
            <div class="text-[10px] uppercase tracking-wider text-slate-500 mb-2">Observed backend API calls</div>
            <div v-if="relatedApis.length" v-for="api in relatedApis" :key="api.id" class="py-2 border-b border-slate-800 text-[10px]"><div class="text-emerald-300">{{ api.method }} {{ api.path }}</div><div class="text-slate-500">{{ api.source || 'Backend source not recorded' }}</div></div>
            <div v-else class="text-[10px] text-slate-500 leading-5">No exact endpoint match was discovered for the observed preview requests. No backend relationship is inferred.</div>
            <div v-if="resourcePaths.length" class="mt-3 text-[9px] text-slate-600">{{ resourcePaths.length }} observed API resource URLs in preview performance entries.</div>
          </div>
        </template>
      </aside>
    </div>
  </section>
</template>
