<!-- src/components/Automation/ActionPanel.vue -->
<!-- <script setup>
// ==================================================
// 📦 Props & Emits
// ==================================================
const props = defineProps({
  selectedNode: { type: Object, default: null },
  show: { type: Boolean, default: false },
  newActionTypeForPanel: { type: String, default: 'open_program' },
})

const emit = defineEmits([
  'close',
  'update:newActionTypeForPanel',
  'create-action',
  'update-action',
  'delete-action',
])

// ==================================================
// 🎨 Action Options
// ==================================================
const actionOptions = [
  { value: 'open_program', label: '🖥️ Open Program' },
  { value: 'close_program', label: '❌ Close Program' },
  { value: 'press', label: '🖱️ Press Key' },
  { value: 'typing', label: '⌨️ Typing' },
  { value: 'wait', label: '⏳ Wait' },
  { value: 'hotkey', label: '🔥 Hotkey' },
  { value: 'click_element', label: '🎯 Click Element' },
]

// ==================================================
// 🔑 Helper — اجيب الـ backend_id الصح
// ==================================================
const getNodeId = () => props.selectedNode?.data?.node?.backend_id ?? props.selectedNode?.id
</script>

<template>
  <transition name="slide">
    <div v-if="show && selectedNode" class="action-panel">
      <div class="panel-header">
        <div>
          <div class="panel-label">SELECTED NODE</div>
          <div class="panel-title">
            {{ selectedNode.data?.node?.program_name ?? selectedNode.data?.node?.label }}
          </div>
          <div class="panel-subtitle">
            {{ selectedNode.data?.node?.node_type }}
          </div>
        </div>
        <button class="panel-close" @click="emit('close')">✕</button>
      </div>

      <hr class="panel-divider" />

      <div class="panel-section-title">
        ⚡ ACTIONS ({{ selectedNode.data?.actions?.length ?? 0 }})
      </div>

      <div v-for="action in selectedNode.data?.actions ?? []" :key="action.id" class="action-item">
        <div class="action-id">ID: {{ action.id?.slice(0, 8) }}...</div>

        <select
          :value="action.action_type"
          class="action-select"
          @change="
            emit('update-action', {
              nodeId: getNodeId(),
              actionId: action.id,
              newActionType: $event.target.value,
            })
          "
        >
          <option v-for="opt in actionOptions" :key="opt.value" :value="opt.value">
            {{ opt.label }}
          </option>
        </select>

        <button
          class="action-delete-btn"
          @click="emit('delete-action', { nodeId: getNodeId(), actionId: action.id })"
        >
          🗑️ Delete Action
        </button>
      </div>

      <div class="action-add-box">
        <div class="action-add-title">➕ Add New Action</div>

        <select
          :value="newActionTypeForPanel"
          class="action-select action-select--blue"
          @change="emit('update:newActionTypeForPanel', $event.target.value)"
        >
          <option v-for="opt in actionOptions" :key="opt.value" :value="opt.value">
            {{ opt.label }}
          </option>
        </select>

        <button
          class="action-create-btn"
          @click="
            emit('create-action', {
              nodeId: getNodeId(),
              action_type: newActionTypeForPanel,
            })
          "
        >
          ✅ Create Action
        </button>
      </div>
    </div>
  </transition>
</template>

<style scoped>
/* ===== Panel Container ===== */
.action-panel {
  position: fixed;
  top: 0;
  right: 0;
  width: 320px;
  height: 100vh;
  background: #0f172a;
  border-left: 1px solid #334155;
  padding: 20px;
  overflow-y: auto;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* ===== Header ===== */
.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.panel-label {
  color: #94a3b8;
  font-size: 0.75rem;
}
.panel-title {
  color: #e2e8f0;
  font-weight: bold;
  font-size: 1rem;
}
.panel-subtitle {
  color: #64748b;
  font-size: 0.7rem;
}
.panel-close {
  background: transparent;
  border: none;
  color: #94a3b8;
  font-size: 1.2rem;
  cursor: pointer;
}
.panel-divider {
  border-color: #334155;
}

/* ===== Section Title ===== */
.panel-section-title {
  color: #94a3b8;
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.05em;
}

/* ===== Action Item ===== */
.action-item {
  background: #1e293b;
  border: 1px solid #334155;
  border-radius: 8px;
  padding: 10px;
}
.action-id {
  color: #94a3b8;
  font-size: 0.7rem;
  margin-bottom: 6px;
}
.action-delete-btn {
  background: #7f1d1d;
  color: #fca5a5;
  border: none;
  border-radius: 6px;
  padding: 4px 10px;
  font-size: 0.75rem;
  cursor: pointer;
  width: 100%;
  margin-top: 6px;
}

/* ===== Select ===== */
.action-select {
  width: 100%;
  background: #0f172a;
  color: #e2e8f0;
  border: 1px solid #334155;
  border-radius: 6px;
  padding: 6px 10px;
  font-size: 0.8rem;
  cursor: pointer;
  margin-bottom: 6px;
}
.action-select--blue {
  border-color: #3b82f6;
  margin-bottom: 8px;
}

/* ===== Add Box ===== */
.action-add-box {
  background: #1e3a5f;
  border: 1px dashed #3b82f6;
  border-radius: 8px;
  padding: 12px;
}
.action-add-title {
  color: #93c5fd;
  font-size: 0.8rem;
  font-weight: 600;
  margin-bottom: 8px;
}
.action-create-btn {
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 8px;
  width: 100%;
  cursor: pointer;
  font-size: 0.85rem;
}

/* ===== Transition ===== */
.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease;
}
.slide-enter-from,
.slide-leave-to {
  transform: translateX(100%);
}
</style>
 -->

<script setup>
import { computed } from 'vue'

// ══════════════════════════════════════════════════
// PROPS & EMITS
// ══════════════════════════════════════════════════
const props = defineProps({
  selectedNode: { type: Object, default: null },
  show: { type: Boolean, default: false },
  newActionTypeForPanel: { type: String, default: 'open_program' },
})

const emit = defineEmits([
  'close',
  'update:newActionTypeForPanel',
  'create-action',
  'update-action',
  'delete-action',
])

// ══════════════════════════════════════════════════
// NODE TYPE — نفس المنطق بتاع CustomNode
// ══════════════════════════════════════════════════
const nodeType = computed(() => props.selectedNode?.data?.node?.node_type?.toLowerCase() ?? '')
const isProgramNode = computed(() => nodeType.value === 'program')
const isProgramElementNode = computed(() => nodeType.value === 'program-element')
const isDelayNode = computed(() => ['delay', 'timing', 'wait'].includes(nodeType.value))

// ══════════════════════════════════════════════════
// ACTION OPTIONS — حسب نوع النود
// ══════════════════════════════════════════════════
const ACTION_OPTIONS = {
  program: [
    { value: 'open_program', label: '▶️  Open Program' },
    { value: 'close_program', label: '⏹️  Close Program' },
    { value: 'focus', label: '🎯  Focus Window' },
    { value: 'maximize', label: '⛶   Maximize' },
    { value: 'get_program_status', label: '📊  Get Status' },
  ],
  'program-element': [
    { value: 'press', label: '🖱️  Click / Press' },
    { value: 'typing', label: '⌨️  Type Text' },
    { value: 'double_click', label: '🖱️  Double Click' },
    { value: 'right_click', label: '🖱️  Right Click' },
    { value: 'hover', label: '🎯  Hover' },
    { value: 'keyboard_shortcut', label: '⌨️  Keyboard Shortcut' },
  ],
  delay: [{ value: 'wait', label: '⏳  Wait' }],
  default: [
    { value: 'open_program', label: '▶️  Open Program' },
    { value: 'close_program', label: '⏹️  Close Program' },
    { value: 'press', label: '🖱️  Click / Press' },
    { value: 'typing', label: '⌨️  Type Text' },
    { value: 'wait', label: '⏳  Wait' },
    { value: 'hotkey', label: '🔥  Hotkey' },
    { value: 'keyboard_shortcut', label: '⌨️  Keyboard Shortcut' },
    { value: 'hover', label: '🎯  Hover' },
    { value: 'double_click', label: '🖱️  Double Click' },
  ],
}

const currentOptions = computed(() => {
  const key = nodeType.value
  return ACTION_OPTIONS[key] ?? ACTION_OPTIONS.default
})

// ══════════════════════════════════════════════════
// NODE DATA HELPERS
// ══════════════════════════════════════════════════
const nodeData = computed(() => props.selectedNode?.data ?? {})
const node = computed(() => nodeData.value.node ?? {})
const actions = computed(() => nodeData.value.actions ?? [])
const elementMeta = computed(() => {
  const n = node.value
  if (n?.element && typeof n.element === 'object') return n.element
  return {
    element_type: n?.element_type ?? '',
    automation_id: n?.automation_id ?? '',
    keyboard_shortcut: n?.keyboard_shortcut ?? '',
    x_coordinate: n?.x_coordinate ?? null,
    y_coordinate: n?.y_coordinate ?? null,
    width: n?.width ?? null,
    height: n?.height ?? null,
    stability_score: n?.stability_score ?? 1.0,
  }
})

const getNodeId = () => node.value.backend_id ?? props.selectedNode?.id

// Stability
const stabilityPercent = computed(() => Math.round((elementMeta.value.stability_score ?? 1) * 100))
const stabilityColor = computed(() => {
  const s = elementMeta.value.stability_score ?? 1
  if (s >= 0.8) return '#16a34a'
  if (s >= 0.5) return '#f59e0b'
  return '#dc2626'
})

// ══════════════════════════════════════════════════
// PAYLOAD NEEDS — بيحدد هل الأكشن محتاج input
// ══════════════════════════════════════════════════
const PAYLOAD_NEEDS_TEXT = ['typing', 'keyboard_shortcut', 'hotkey']
const PAYLOAD_NEEDS_SECONDS = ['wait']

const actionNeedsText = (type) => PAYLOAD_NEEDS_TEXT.includes(type)
const actionNeedsSeconds = (type) => PAYLOAD_NEEDS_SECONDS.includes(type)
</script>

<template>
  <transition name="slide">
    <div v-if="show && selectedNode" class="action-panel">
      <!-- ══════════════════════════════════════
      HEADER
      ══════════════════════════════════════ -->
      <div class="panel-header">
        <div class="panel-header__info">
          <!-- Node Type Badge -->
          <span class="panel-type-badge" :class="`badge--${nodeType}`">
            <i
              :class="{
                'pi pi-desktop': isProgramNode,
                'pi pi-bolt': isProgramElementNode,
                'pi pi-clock': isDelayNode,
                'pi pi-circle': !isProgramNode && !isProgramElementNode && !isDelayNode,
              }"
            />
            {{ nodeType || 'node' }}
          </span>

          <!-- Node Title -->
          <div class="panel-title">
            {{ node.program_name ?? node.element_name ?? node.label ?? '—' }}
          </div>

          <!-- Element Info (لو program-element) -->
          <template v-if="isProgramElementNode">
            <div class="panel-subtitle">
              <i class="pi pi-desktop" style="font-size: 10px" />
              {{ node.program_name ?? '—' }}
            </div>
            <div class="panel-element-meta">
              <span v-if="elementMeta.element_type" class="meta-pill">
                {{ elementMeta.element_type }}
              </span>
              <span v-if="elementMeta.keyboard_shortcut" class="meta-shortcut">
                ⌨ {{ elementMeta.keyboard_shortcut }}
              </span>
              <span class="meta-stability" :style="{ color: stabilityColor }">
                ● {{ stabilityPercent }}%
              </span>
            </div>
            <div v-if="elementMeta.automation_id" class="meta-id">
              ID: {{ elementMeta.automation_id }}
            </div>
          </template>

          <!-- Program Info -->
          <div v-else-if="isProgramNode" class="panel-subtitle">
            <i class="pi pi-folder" style="font-size: 10px" />
            {{ node.program_name ?? '—' }}
          </div>
        </div>
        <button class="panel-close" @click="emit('close')">✕</button>
      </div>

      <div class="panel-divider" />

      <!-- ══════════════════════════════════════
      EXISTING ACTIONS
      ══════════════════════════════════════ -->
      <div class="panel-section-title">
        ⚡ ACTIONS
        <span class="action-count">{{ actions.length }}</span>
      </div>

      <div v-if="actions.length === 0" class="empty-actions">No actions yet — add one below</div>

      <div v-for="action in actions" :key="action.id" class="action-item">
        <!-- Action ID -->
        <div class="action-item__header">
          <code class="action-id">{{ action.id?.slice(0, 8) }}…</code>
          <button
            class="btn-delete-action"
            title="Delete Action"
            @click="
              emit('delete-action', {
                nodeId: getNodeId(),
                actionId: action.id,
              })
            "
          >
            🗑
          </button>
        </div>

        <!-- Action Type Select -->
        <label class="field-label">Action Type</label>
        <select
          :value="action.action_type"
          class="field-select"
          @change="
            emit('update-action', {
              nodeId: getNodeId(),
              actionId: action.id,
              newActionType: $event.target.value,
            })
          "
        >
          <option v-for="opt in currentOptions" :key="opt.value" :value="opt.value">
            {{ opt.label }}
          </option>
        </select>

        <!-- Payload: Text -->
        <template v-if="actionNeedsText(action.action_type)">
          <label class="field-label">Text</label>
          <input
            type="text"
            class="field-input"
            :placeholder="
              action.action_type === 'keyboard_shortcut' ? 'e.g. ctrl+s' : 'Enter text to type…'
            "
            :value="action.payload?.text ?? ''"
            @change="
              emit('update-action', {
                nodeId: getNodeId(),
                actionId: action.id,
                newActionType: action.action_type,
                payload: { text: $event.target.value },
              })
            "
          />
        </template>

        <!-- Payload: Seconds -->
        <template v-if="actionNeedsSeconds(action.action_type)">
          <label class="field-label">Duration (seconds)</label>
          <input
            type="number"
            min="0"
            step="0.1"
            class="field-input field-input--number"
            :value="action.payload?.seconds ?? 1"
            @change="
              emit('update-action', {
                nodeId: getNodeId(),
                actionId: action.id,
                newActionType: action.action_type,
                payload: { seconds: parseFloat($event.target.value) },
              })
            "
          />
        </template>

        <!-- Payload Preview -->
        <div v-if="action.payload && Object.keys(action.payload).length" class="payload-preview">
          <span v-for="(val, key) in action.payload" :key="key" class="payload-tag">
            {{ key }}: <strong>{{ val }}</strong>
          </span>
        </div>
      </div>

      <!-- ══════════════════════════════════════
      ADD NEW ACTION
      ══════════════════════════════════════ -->
      <div class="add-action-box">
        <div class="add-action-title">➕ Add New Action</div>

        <label class="field-label">Action Type</label>
        <select
          :value="newActionTypeForPanel"
          class="field-select field-select--blue"
          @change="emit('update:newActionTypeForPanel', $event.target.value)"
        >
          <option v-for="opt in currentOptions" :key="opt.value" :value="opt.value">
            {{ opt.label }}
          </option>
        </select>

        <button
          class="btn-create"
          @click="
            emit('create-action', {
              nodeId: getNodeId(),
              action_type: newActionTypeForPanel,
            })
          "
        >
          ✅ Create Action
        </button>
      </div>
    </div>
  </transition>
</template>

<style scoped lang="scss">
/* ── Panel ──────────────────────────────────── */
.action-panel {
  position: fixed;
  top: 0;
  right: 0;
  width: 300px;
  height: 100vh;
  background: #0b1120;
  border-left: 1px solid #1e293b;
  padding: 16px;
  overflow-y: auto;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  gap: 10px;
  font-size: 12px;
  color: #e2e8f0;
}

/* ── Header ─────────────────────────────────── */
.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 8px;
}
.panel-header__info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.panel-type-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  padding: 2px 7px;
  border-radius: 4px;
  width: fit-content;
}
.badge--program {
  background: rgba(22, 163, 74, 0.2);
  color: #86efac;
}
.badge--program-element {
  background: rgba(99, 102, 241, 0.2);
  color: #a5b4fc;
}
.badge--delay,
.badge--timing,
.badge--wait {
  background: rgba(100, 116, 139, 0.2);
  color: #94a3b8;
}
.badge--typing {
  background: rgba(250, 204, 21, 0.15);
  color: #fde047;
}

.panel-title {
  font-size: 14px;
  font-weight: 700;
  color: #f1f5f9;
  line-height: 1.3;
}
.panel-subtitle {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #64748b;
  font-size: 11px;
}
.panel-element-meta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 5px;
  margin-top: 2px;
}
.meta-pill {
  font-size: 9px;
  padding: 1px 5px;
  border-radius: 3px;
  background: rgba(99, 102, 241, 0.2);
  color: #a5b4fc;
  font-weight: 600;
  text-transform: uppercase;
}
.meta-shortcut {
  font-size: 10px;
  font-family: monospace;
  color: #facc15;
}
.meta-stability {
  font-size: 10px;
  font-weight: 600;
}
.meta-id {
  font-size: 10px;
  font-family: monospace;
  color: #475569;
}

.panel-close {
  background: transparent;
  border: none;
  color: #475569;
  font-size: 16px;
  cursor: pointer;
  padding: 0;
  line-height: 1;
  flex-shrink: 0;
  &:hover {
    color: #e2e8f0;
  }
}

/* ── Divider ─────────────────────────────────── */
.panel-divider {
  height: 1px;
  background: #1e293b;
  margin: 2px 0;
}

/* ── Section Title ───────────────────────────── */
.panel-section-title {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #64748b;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.6px;
}
.action-count {
  background: #1e293b;
  color: #94a3b8;
  border-radius: 10px;
  padding: 0 6px;
  font-size: 10px;
}
.empty-actions {
  color: #334155;
  font-size: 11px;
  text-align: center;
  padding: 12px 0;
  border: 1px dashed #1e293b;
  border-radius: 8px;
}

/* ── Action Item ─────────────────────────────── */
.action-item {
  background: #0f172a;
  border: 1px solid #1e293b;
  border-radius: 8px;
  padding: 10px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.action-item__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.action-id {
  font-size: 10px;
  color: #334155;
  font-family: monospace;
}
.btn-delete-action {
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: 13px;
  opacity: 0.5;
  padding: 0;
  &:hover {
    opacity: 1;
  }
}

/* ── Fields ──────────────────────────────────── */
.field-label {
  font-size: 10px;
  color: #475569;
  text-transform: uppercase;
  letter-spacing: 0.4px;
}
.field-select {
  width: 100%;
  background: #1e293b;
  color: #e2e8f0;
  border: 1px solid #334155;
  border-radius: 6px;
  padding: 5px 8px;
  font-size: 11px;
  cursor: pointer;
  &:focus {
    outline: none;
    border-color: #6366f1;
  }
  option {
    background: #0f172a;
  }
}
.field-select--blue {
  border-color: #3b82f6;
}

.field-input {
  width: 100%;
  background: #1e293b;
  color: #e2e8f0;
  border: 1px solid #334155;
  border-radius: 6px;
  padding: 5px 8px;
  font-size: 11px;
  box-sizing: border-box;
  &:focus {
    outline: none;
    border-color: #6366f1;
  }
  &::placeholder {
    color: #334155;
  }
}
.field-input--number {
  width: 80px;
}

/* ── Payload Preview ─────────────────────────── */
.payload-preview {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-top: 2px;
}
.payload-tag {
  font-size: 9px;
  background: #1e293b;
  color: #64748b;
  padding: 1px 6px;
  border-radius: 4px;
  font-family: monospace;
  strong {
    color: #94a3b8;
  }
}

/* ── Add Action Box ──────────────────────────── */
.add-action-box {
  background: #0d1f35;
  border: 1px dashed #2563eb;
  border-radius: 8px;
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-top: auto;
}
.add-action-title {
  color: #60a5fa;
  font-size: 11px;
  font-weight: 600;
}
.btn-create {
  background: #2563eb;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 7px;
  width: 100%;
  cursor: pointer;
  font-size: 12px;
  font-weight: 600;
  &:hover {
    background: #1d4ed8;
  }
}

/* ── Transition ──────────────────────────────── */
.slide-enter-active,
.slide-leave-active {
  transition: transform 0.25s ease;
}
.slide-enter-from,
.slide-leave-to {
  transform: translateX(100%);
}
</style>
