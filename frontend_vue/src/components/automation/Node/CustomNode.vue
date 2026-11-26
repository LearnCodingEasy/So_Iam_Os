<!--

<script setup>
/**
 * 🧠 هذا الكومبوننت يمثل Node داخل Workflow Automation System
 * يمكن أن يكون:
 *
 * 🖥 Program Node
 * ⏱ Delay Node
 * ⌨ Typing Node
 *
 * ويعرض بيانات النود + يسمح بتعديل الأكشن.
 */

// ==================================================
// 📦 IMPORTS
// ==================================================
// 📚 Vue Core
import { ref, watch, computed } from 'vue'
// 📚 VueFlow (لإنشاء Graph Nodes)
import { Handle, Position } from '@vue-flow/core'

// ==================================================
// 📥 PROPS
// ==================================================

// ==================================================
// 📤 EVENTS
// ==================================================


// ==================================================
// 📦 COMPUTED DATA STRUCTURE
// ==================================================

// ==================================================
// 🧠 LOCAL STATE
// ==================================================

/**
 * هذه القيم تمثل الحالة المحلية للنود داخل الواجهة
 */

const localAction = ref(props.data?.action?.action_type ?? 'open_program') // ⚙ نوع الأكشن

const localDelay = ref(props.data?.config?.delay ?? 0) // ⏱ قيمة التأخير

const localTypingText = ref(props.data?.config?.text ?? '') // ⌨ النص المكتوب

// ==================================================
// 🎨 COMPUTED UI STATES
// ==================================================

/**
 * 🧩 nodeTypeClass()
 * 🎯 تحديد كلاس CSS حسب نوع النود
 */

const nodeTypeClass = computed(() => {
  const type = node.value.node_type?.toLowerCase()

  if (type === 'program') return 'open_program'

  if (type === 'delay' || type === 'timing') return 'node-delay'

  return 'node-default'
})

/**
 * 🎨 dynamicIcon()
 * 🎯 تحديد الأيقونة حسب نوع النود
 */

const dynamicIcon = computed(() => {
  const type = node.value.node_type

  if (type === 'program') return 'pi pi-desktop'

  if (type === 'delay') return 'pi pi-clock'

  return 'pi pi-circle'
})

/**
 * 🧠 isProgramNode
 * 🎯 هل النود خاص ببرنامج؟
 */

const isProgramNode = computed(() => node.value.node_type?.toLowerCase() === 'program')

/**
 * 🧠 isProgramNode
 * 🎯 هل النود خاص بعنصر برنامج؟
 */

const isProgramElementNode = computed(
  () => node.value.node_type?.toLowerCase() === 'program-element',
)

/**
 * ⏱ isDelayNode
 * 🎯 هل النود يمثل Delay؟
 */

const isDelayNode = computed(() => {
  const type = node.value.node_type?.toLowerCase()

  return type === 'delay' || type === 'timing'
})

/**
 * 🎨 actionColor
 * 🎯 تحديد لون النود حسب الأكشن
 */

const actionColor = computed(() => {
  switch (localAction.value) {
    case 'open_program':
      return '#16a34a' // 🟢 أخضر

    case 'close_program':
      return '#dc2626' // 🔴 أحمر

    case 'get_program_status':
      return '#0ea5e9' // 🔵 أزرق

    case 'focus':
      return '#f59e0b' // 🟠 برتقالي

    case 'maximize':
      return '#8b5cf6' // 🟣 بنفسجي

    case 'press':
      return '#64748b' // ⚫ رمادي

    case 'typing':
      return '#facc15' // 🟡 أصفر

    default:
      return '#334155'
  }
})

/**
 * 🏃‍♂️ isRunningAction
 * 🎯 تحديد هل الأكشن يعمل الآن
 */

const isRunningAction = computed(() =>
  ['open_program', 'close_program', 'press', 'typing'].includes(localAction.value),
)

/**
 * 📊 statusClass
 * 🎯 تحديد حالة النود
 */

const statusClass = computed(() => ({
  running: props.data.status === 'open',
  stopped: props.data.status === 'closed',
}))
console.log('statusClass: ', statusClass)

// ==================================================
// ⚙ METHODS
// ==================================================

/**
 * ⚙ updateAction()
 *
 * 🎯 تحديث الأكشن الخاص بالنود
 *
 * 📥 المدخلات:
 * لا يوجد (يعتمد على local state)
 *
 * 📤 المخرجات:
 * إرسال حدث إلى الـ Parent
 *
 * 🧠 المنطق:
 * إرسال نوع الأكشن الجديد مع بيانات إضافية
 */

const updateAction = () => {
  const payload = {
    nodeId: props.data?.node.backend_id,

    newActionType: localAction.value,

    extraData: localAction.value === 'typing' ? { text: localTypingText.value } : {},
  }

  emit('update-node-action', payload)
}

/**
 * ⌨ updateTypingAction()
 *
 * 🎯 تحديث النص عند الكتابة
 */

const updateTypingAction = () => {
  if (localAction.value === 'typing') {
    updateAction()
  }
}

/**
 * ⏱ updateDelay()
 *
 * 🎯 تحديث قيمة التأخير
 */

const updateDelay = () => {
  emit('update-node-action', {
    nodeId: props.data.backend_id,

    newActionType: localAction.value,

    extraData: { delay: localDelay.value },
  })
}
// ==================================================
// 👀 WATCHERS
// ==================================================

/**
 * 👀 مراقبة تغير الأكشن من الخارج
 */

watch(
  () => node.value?.config?.action,
  (v) => {
    if (v) localAction.value = v
  },
)

/**
 * 👀 مراقبة النص الخاص بالكتابة
 */

watch(
  () => props.data?.node?.config?.text,
  (v) => {
    localTypingText.value = v ?? ''
  },
)
</script>

<style lang="scss">
</style>
 -->

<template>
  <div
    class="node"
    :class="[nodeTypeClass, { 'node--running': isRunningAction }]"
    :style="nodeStyle"
  >
    <!-- ══════════════════════════════════════
    HEADER — اسم النود + نوعه + أيقونته
    ══════════════════════════════════════ -->
    <div class="node-header" :style="{ borderColor: accentColor }">
      <div class="node-header__left">
        <span class="node-icon" :style="{ background: accentColor }">
          <i :class="dynamicIcon" />
        </span>
        <div class="node-header__text">
          <span class="node-title">{{ nodeTitle }}</span>
          <span class="node-type-badge" :style="{ color: accentColor }">
            {{ nodeTypeLabel }}
          </span>
        </div>
      </div>

      <!-- مؤشر الـ stability لـ program-element -->
      <div
        v-if="isProgramElementNode"
        class="stability-indicator"
        :title="`Stability: ${stabilityPercent}%`"
      >
        <span class="stability-dot" :class="stabilityClass" />
      </div>
    </div>

    <!-- ══════════════════════════════════════
    BODY — المحتوى حسب نوع النود
    ══════════════════════════════════════ -->
    <div class="node-body">
      <!-- 🖥 PROGRAM NODE -->
      <template v-if="isProgramNode">
        <div class="node-info-row">
          <i class="pi pi-folder node-info-icon" />
          <span>{{ node.program_name ?? '—' }}</span>
        </div>
        <div class="node-action-row">
          <label class="node-label">Action</label>
          <select v-model="localAction" @change="updateAction" class="node-select">
            <option value="open_program">▶️ Open Program</option>
            <option value="close_program">⏹️ Close Program</option>
            <option value="focus">🎯 Focus Window</option>
            <option value="maximize">⛶ Maximize</option>
            <option value="get_program_status">📊 Status</option>
          </select>
        </div>
      </template>

      <!-- ⚡ PROGRAM-ELEMENT NODE -->
      <template v-else-if="isProgramElementNode">
        <div class="node-info-row">
          <i class="pi pi-desktop node-info-icon" />
          <span>{{ node.program_name ?? '—' }}</span>
        </div>
        <div class="node-info-row node-info-row--highlight">
          <i class="pi pi-bolt node-info-icon" />
          <span>{{ node.element_name ?? '—' }}</span>
        </div>

        <!-- تفاصيل العنصر -->
        <div class="node-element-meta">
          <span v-if="elementMeta.element_type" class="meta-tag">
            {{ elementMeta.element_type }}
          </span>
          <span v-if="elementMeta.keyboard_shortcut" class="meta-shortcut">
            <i class="pi pi-keyboard" /> {{ elementMeta.keyboard_shortcut }}
          </span>
          <span v-if="elementMeta.automation_id" class="meta-id">
            {{ elementMeta.automation_id }}
          </span>
        </div>

        <!-- الإحداثيات لو موجودة -->
        <div v-if="elementMeta.x_coordinate || elementMeta.y_coordinate" class="node-coords">
          <i class="pi pi-map-marker node-info-icon" />
          <span>{{ elementMeta.x_coordinate }}, {{ elementMeta.y_coordinate }}</span>
          <span v-if="elementMeta.width" class="meta-id">
            {{ elementMeta.width }}×{{ elementMeta.height }}px
          </span>
        </div>

        <!-- الـ Action الخاص بالعنصر -->
        <div class="node-action-row">
          <label class="node-label">Action</label>
          <select v-model="localAction" @change="updateAction" class="node-select">
            <option value="press">🖱️ Click / Press</option>
            <option value="typing">⌨️ Type Text</option>
            <option value="double_click">🖱️ Double Click</option>
            <option value="right_click">🖱️ Right Click</option>
            <option value="hover">🎯 Hover</option>
            <option value="keyboard_shortcut">⌨️ Keyboard Shortcut</option>
          </select>
        </div>

        <!-- حقل النص لو typing -->
        <div v-if="localAction === 'typing'" class="node-typing-input">
          <input
            v-model="localTypingText"
            @input="updateTypingAction"
            placeholder="Enter text to type..."
            class="node-input"
          />
        </div>
      </template>

      <!-- ⏱ DELAY NODE -->
      <template v-else-if="isDelayNode">
        <div class="node-info-row">
          <i class="pi pi-clock node-info-icon" />
          <span>Wait for</span>
        </div>
        <div class="node-delay-config">
          <input
            type="number"
            min="0"
            step="0.1"
            v-model="localDelay"
            @change="updateDelay"
            class="node-input node-input--delay"
          />
          <span class="delay-unit">seconds</span>
        </div>
      </template>

      <!-- ⌨ TYPING NODE (standalone) -->
      <template v-else-if="isTypingNode">
        <div class="node-info-row">
          <i class="pi pi-pencil node-info-icon" />
          <span>Type Text</span>
        </div>
        <div class="node-typing-input">
          <input
            v-model="localTypingText"
            @input="updateTypingAction"
            placeholder="Enter text to type..."
            class="node-input"
          />
        </div>
      </template>

      <!-- 🔵 DEFAULT / PLUGIN NODE -->
      <template v-else>
        <div class="node-info-row">
          <i class="pi pi-cog node-info-icon" />
          <span>{{ node.node_type ?? 'Custom' }}</span>
        </div>
        <div v-if="primaryAction" class="node-info-row">
          <i class="pi pi-play node-info-icon" />
          <span>{{ primaryAction.action_type }}</span>
        </div>
      </template>
    </div>

    <!-- ══════════════════════════════════════
        FOOTER — أزرار التحكم حسب النوع
    ══════════════════════════════════════ -->
    <div class="node-footer">
      <!-- Program -->
      <template v-if="isProgramNode">
        <button class="node-btn node-btn--run" @click="$emit('run-task', data)">▶ Run</button>
        <button class="node-btn" @click="$emit('open-program', node.program)">Open</button>
        <button class="node-btn node-btn--danger" @click="$emit('close-program', node.program)">
          Close
        </button>
        <button class="node-btn node-btn--ghost" @click="$emit('delete-node', node.backend_id)">
          🗑
        </button>
      </template>

      <!-- Program-Element -->
      <template v-else-if="isProgramElementNode">
        <button class="node-btn node-btn--run" @click="$emit('run-task', data)">▶ Run</button>
        <button class="node-btn node-btn--ghost" @click="$emit('delete-node', node.backend_id)">
          🗑
        </button>
      </template>

      <!-- Delay / Typing / Default -->
      <template v-else>
        <button class="node-btn node-btn--ghost" @click="$emit('delete-node', node.backend_id)">
          🗑
        </button>
      </template>
    </div>

    <!-- ══════════════════════════════════════
    HANDLES — نقاط الربط
    ══════════════════════════════════════ -->
    <Handle type="target" :position="Position.Left" id="target" />
    <Handle type="source" :position="Position.Right" id="source" />
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { Handle, Position } from '@vue-flow/core'

// ══════════════════════════════════════════════════
// PROPS & EMITS
// ══════════════════════════════════════════════════
/* 📦 props.data   Backend  يحتوي على بيانات النود القادمة من  */
const props = defineProps({
  data: { type: Object, default: () => ({}) },
})
/* 🚀 Parent Component الأحداث التي يمكن إرسالها إلى الـ  */
const emit = defineEmits([
  'update-node-action',
  'run-task',
  'open-program',
  'close-program',
  'status-program',
  'delete-node',
])

// ══════════════════════════════════════════════════
// DATA ACCESSORS
// ══════════════════════════════════════════════════
/*  🧠 نعيد تنظيم البيانات القادمة من
Backend
لتسهيل استخدامها داخل الكومبوننت */
const data = computed(() => props.data ?? {})
const node = computed(() => data.value.node ?? {})
const config = computed(() => node.value.config ?? {})
const actions = computed(() => data.value.actions ?? [])

// أول action — لتحديد اللون الافتراضي
const primaryAction = computed(() => actions.value?.[0] ?? null)

// ══════════════════════════════════════════════════
// NODE TYPE FLAGS
// ══════════════════════════════════════════════════

const nodeType = computed(() => node.value.node_type?.toLowerCase() ?? '')

const isProgramNode = computed(() => nodeType.value === 'program')
const isProgramElementNode = computed(() => nodeType.value === 'program-element')
const isDelayNode = computed(() => ['delay', 'timing', 'wait'].includes(nodeType.value))
const isTypingNode = computed(() => nodeType.value === 'typing')

// ══════════════════════════════════════════════════
// ELEMENT META — بيانات العنصر المرتبط
// ══════════════════════════════════════════════════

const elementMeta = computed(() => {
  const n = node.value
  // الـ backend الجديد بيبعت element كـ nested object
  if (n?.element && typeof n.element === 'object') return n.element
  // fallback على الحقول المباشرة في node
  return {
    element_type: n?.element_type ?? '',
    automation_id: n?.automation_id ?? '',
    keyboard_shortcut: n?.keyboard_shortcut ?? '',
    selector_type: n?.selector_type ?? '',
    selector_value: n?.selector_value ?? '',
    x_coordinate: n?.x_coordinate ?? null,
    y_coordinate: n?.y_coordinate ?? null,
    width: n?.width ?? null,
    height: n?.height ?? null,
    stability_score: n?.stability_score ?? 1.0,
  }
})

// Stability
const stabilityPercent = computed(() => Math.round((elementMeta.value.stability_score ?? 1) * 100))
const stabilityClass = computed(() => {
  const s = elementMeta.value.stability_score ?? 1
  if (s >= 0.8) return 'high'
  if (s >= 0.5) return 'medium'
  return 'low'
})

// ══════════════════════════════════════════════════
// UI LABELS & ICONS
// ══════════════════════════════════════════════════

const nodeTypeLabel = computed(() => {
  if (isProgramNode.value) return 'Program'
  if (isProgramElementNode.value) return 'UI Element'
  if (isDelayNode.value) return 'Delay'
  if (isTypingNode.value) return 'Typing'
  return node.value.node_type ?? 'Custom'
})

const nodeTitle = computed(() => {
  if (isProgramNode.value) return node.value.program_name ?? node.value.label ?? '—'
  if (isProgramElementNode.value) return node.value.element_name ?? node.value.label ?? '—'
  if (isDelayNode.value) return `Wait ${localDelay.value}s`
  return node.value.label ?? 'Node'
})

const dynamicIcon = computed(() => {
  if (isProgramNode.value) return 'pi pi-desktop'
  if (isProgramElementNode.value) return 'pi pi-bolt'
  if (isDelayNode.value) return 'pi pi-clock'
  if (isTypingNode.value) return 'pi pi-pencil'
  return 'pi pi-circle'
})

const nodeTypeClass = computed(() => {
  if (isProgramNode.value) return 'node--program'
  if (isProgramElementNode.value) return 'node--element'
  if (isDelayNode.value) return 'node--delay'
  if (isTypingNode.value) return 'node--typing'
  return 'node--default'
})

// ══════════════════════════════════════════════════
// ACCENT COLOR — لون مميز لكل نوع
// ══════════════════════════════════════════════════

const ACTION_COLORS = {
  open_program: '#16a34a',
  close_program: '#dc2626',
  get_program_status: '#0ea5e9',
  focus: '#f59e0b',
  maximize: '#8b5cf6',
  press: '#6366f1',
  double_click: '#6366f1',
  right_click: '#6366f1',
  hover: '#06b6d4',
  keyboard_shortcut: '#facc15',
  typing: '#facc15',
  wait: '#64748b',
}

const TYPE_COLORS = {
  'node--program': '#16a34a',
  'node--element': '#6366f1',
  'node--delay': '#64748b',
  'node--typing': '#facc15',
  'node--default': '#334155',
}

const accentColor = computed(() => {
  // لو فيه action → لونه
  const actionType = localAction.value || primaryAction.value?.action_type
  if (actionType && ACTION_COLORS[actionType]) return ACTION_COLORS[actionType]
  // fallback على نوع النود
  return TYPE_COLORS[nodeTypeClass.value] ?? '#334155'
})

const nodeStyle = computed(() => ({
  background: node.value.config?.ui?.theme?.background ?? '#0f172a',
  boxShadow: `0 0 12px ${accentColor.value}33`,
  width: (node.value.config?.ui?.layout?.width ?? 220) + 'px',
  borderLeft: `3px solid ${accentColor.value}`,
}))

const isRunningAction = computed(() =>
  ['open_program', 'close_program', 'press', 'typing', 'double_click'].includes(localAction.value),
)

// ══════════════════════════════════════════════════
// LOCAL STATE
// ══════════════════════════════════════════════════

// نحدد الـ default action حسب نوع النود
const defaultAction = () => {
  if (isProgramNode.value) return 'open_program'
  if (isProgramElementNode.value) return 'press'
  if (isDelayNode.value) return 'wait'
  if (isTypingNode.value) return 'typing'
  return primaryAction.value?.action_type ?? 'custom'
}

const localAction = ref(primaryAction.value?.action_type ?? defaultAction())
const localDelay = ref(primaryAction.value?.payload?.seconds ?? 1)
const localTypingText = ref(primaryAction.value?.payload?.text ?? '')

// ══════════════════════════════════════════════════
// METHODS
// ══════════════════════════════════════════════════

const updateAction = () => {
  emit('update-node-action', {
    nodeId: node.value.backend_id,
    actionId: primaryAction.value?.id,
    newActionType: localAction.value,
    extraData: localAction.value === 'typing' ? { text: localTypingText.value } : {},
  })
}

const updateTypingAction = () => {
  if (['typing', 'keyboard_shortcut'].includes(localAction.value)) {
    updateAction()
  }
}

const updateDelay = () => {
  emit('update-node-action', {
    nodeId: node.value.backend_id,
    actionId: primaryAction.value?.id,
    newActionType: 'wait',
    extraData: { seconds: localDelay.value },
  })
}

// ══════════════════════════════════════════════════
// WATCHERS
// ══════════════════════════════════════════════════

// لو الـ actions اتغيرت من الـ store (بعد reload)
watch(
  primaryAction,
  (action) => {
    if (!action) return
    localAction.value = action.action_type ?? defaultAction()
    localDelay.value = action.payload?.seconds ?? localDelay.value
    localTypingText.value = action.payload?.text ?? localTypingText.value
  },
  { immediate: false },
)

watch(
  () => props.data?.node?.config?.text,
  (v) => {
    localTypingText.value = v ?? ''
  },
)
</script>

<style lang="scss" scoped>
// ══════════════════════════════════════
// BASE NODE
// ══════════════════════════════════════
.node {
  border-radius: 8px;
  overflow: hidden;
  color: #e2e8f0;
  font-size: 12px;
  font-family: 'Inter', sans-serif;
  transition: box-shadow 0.2s;
  min-width: 200px;

  &--running {
    animation: pulse 1.5s infinite;
  }
}

// ══════════════════════════════════════
// HEADER
// ══════════════════════════════════════
.node-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 10px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  border-left-width: 0; // الـ border-left على الـ .node نفسه

  &__left {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  &__text {
    display: flex;
    flex-direction: column;
    gap: 1px;
  }
}

.node-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 26px;
  height: 26px;
  border-radius: 6px;
  flex-shrink: 0;

  i {
    font-size: 13px;
    color: #fff;
  }
}

.node-title {
  font-size: 12px;
  font-weight: 600;
  color: #f1f5f9;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 140px;
}

.node-type-badge {
  font-size: 10px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  opacity: 0.85;
}

// ══════════════════════════════════════
// BODY
// ══════════════════════════════════════
.node-body {
  padding: 8px 10px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.node-info-row {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #94a3b8;
  font-size: 11px;

  &--highlight {
    color: #c4b5fd;
    font-weight: 500;
  }
}

.node-info-icon {
  font-size: 10px;
  opacity: 0.6;
  flex-shrink: 0;
}

// ══════════════════════════════════════
// ELEMENT META
// ══════════════════════════════════════
.node-element-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-top: 2px;
}

.meta-tag {
  font-size: 9px;
  padding: 1px 5px;
  border-radius: 4px;
  background: rgba(99, 102, 241, 0.2);
  color: #a5b4fc;
  font-weight: 600;
  text-transform: uppercase;
}

.meta-shortcut {
  font-size: 10px;
  font-family: monospace;
  color: #facc15;
  display: flex;
  align-items: center;
  gap: 3px;
}

.meta-id {
  font-size: 9px;
  color: #475569;
  font-family: monospace;
}

.node-coords {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #475569;
  font-size: 10px;
}

// ══════════════════════════════════════
// STABILITY
// ══════════════════════════════════════
.stability-indicator {
  display: flex;
  align-items: center;
  gap: 4px;
}

.stability-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;

  &.high {
    background: #16a34a;
    box-shadow: 0 0 4px #16a34a88;
  }
  &.medium {
    background: #f59e0b;
    box-shadow: 0 0 4px #f59e0b88;
  }
  &.low {
    background: #dc2626;
    box-shadow: 0 0 4px #dc262688;
  }
}

// ══════════════════════════════════════
// FORM CONTROLS
// ══════════════════════════════════════
.node-label {
  font-size: 10px;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.4px;
}

.node-action-row {
  display: flex;
  flex-direction: column;
  gap: 3px;
  margin-top: 2px;
}

.node-select {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 5px;
  color: #e2e8f0;
  font-size: 11px;
  padding: 4px 6px;
  width: 100%;
  cursor: pointer;

  &:focus {
    outline: none;
    border-color: rgba(99, 102, 241, 0.5);
  }
  option {
    background: #1e293b;
  }
}

.node-input {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 5px;
  color: #e2e8f0;
  font-size: 11px;
  padding: 4px 8px;
  width: 100%;

  &:focus {
    outline: none;
    border-color: rgba(99, 102, 241, 0.5);
  }
  &::placeholder {
    color: #475569;
  }

  &--delay {
    width: 70px;
    text-align: center;
  }
}

.node-delay-config {
  display: flex;
  align-items: center;
  gap: 6px;
}

.delay-unit {
  font-size: 10px;
  color: #64748b;
}

.node-typing-input {
  margin-top: 2px;
}

// ══════════════════════════════════════
// FOOTER
// ══════════════════════════════════════
.node-footer {
  display: flex;
  gap: 4px;
  padding: 6px 10px;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}

.node-btn {
  flex: 1;
  padding: 4px 0;
  border: none;
  border-radius: 5px;
  font-size: 10px;
  font-weight: 500;
  cursor: pointer;
  background: rgba(255, 255, 255, 0.07);
  color: #94a3b8;
  transition: background 0.15s;

  &:hover {
    background: rgba(255, 255, 255, 0.12);
  }

  &--run {
    background: rgba(22, 163, 74, 0.2);
    color: #86efac;
    &:hover {
      background: rgba(22, 163, 74, 0.3);
    }
  }

  &--danger {
    background: rgba(220, 38, 38, 0.15);
    color: #fca5a5;
    &:hover {
      background: rgba(220, 38, 38, 0.25);
    }
  }

  &--ghost {
    flex: 0;
    padding: 4px 8px;
    background: transparent;
    &:hover {
      background: rgba(220, 38, 38, 0.15);
      color: #fca5a5;
    }
  }
}

// ══════════════════════════════════════
// ANIMATIONS
// ══════════════════════════════════════
@keyframes pulse {
  0%,
  100% {
    box-shadow: 0 0 8px currentColor;
  }
  50% {
    box-shadow: 0 0 20px currentColor;
  }
}
</style>
