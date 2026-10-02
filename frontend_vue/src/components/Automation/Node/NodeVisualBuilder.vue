<script setup>
// ============================================================
//  NodeVisualBuilder.vue
//  src/components/Automation/Node/NodeVisualBuilder.vue
//
//  المسؤولية: preview + config للـ node قبل إضافته للـ Canvas
//  الفكرة: المستخدم يضغط "Configure" على plugin →
//          يفتح الـ NodeVisualBuilder لتخصيص الـ node
//
//  الاستخدام:
//    <NodeVisualBuilder
//      :plugin="selectedPlugin"
//      :visible="showBuilder"
//      @confirm="onAddConfiguredNode"
//      @cancel="showBuilder = false"
//    />
//
//  emit('confirm') يرجع:
//    { plugin_id, label, color, payload }
// ============================================================
import { ref, watch, computed } from 'vue'
import registry from '@/plugins/PluginRegistry'

const props = defineProps({
  visible: { type: Boolean, default: false },
  plugin: { type: Object, default: null }, // من PluginRegistry
})

const emit = defineEmits(['confirm', 'cancel', 'update:visible'])

// ─── Form State ───────────────────────────────────────────
const label = ref('')
const customColor = ref('')
const formData = ref({})
const error = ref(null)

// ─── Reset when plugin changes ────────────────────────────
watch(
  () => props.plugin,
  (p) => {
    if (!p) return
    label.value = p.label
    customColor.value = p.color
    formData.value = { ...(p.defaultPayload ?? {}) }
    error.value = null
  },
  { immediate: true },
)

// ─── Node Preview Color ───────────────────────────────────
const nodeColor = computed(() => customColor.value || props.plugin?.color || '#334155')

// ─── Confirm ──────────────────────────────────────────────
const handleConfirm = () => {
  // validate
  if (props.plugin) {
    const validErr = registry.validate(props.plugin.id, formData.value)
    if (validErr) {
      error.value = validErr
      return
    }
  }

  const payload = props.plugin ? registry.buildPayload(props.plugin.id, formData.value) : {}

  emit('confirm', {
    plugin_id: props.plugin?.id,
    label: label.value || props.plugin?.label,
    color: nodeColor.value,
    payload,
  })

  emit('update:visible', false)
}
</script>

<template>
  <prime_dialog
    :visible="visible"
    modal
    :header="`⚙️ تهيئة: ${plugin?.label ?? 'Node'}`"
    :style="{ width: '480px' }"
    @update:visible="$emit('update:visible', $event)"
  >
    <div v-if="plugin" class="builder">
      <!-- ── Node Preview ────────────────────────────── -->
      <div class="builder__preview">
        <div class="node-preview" :style="{ borderColor: nodeColor }">
          <div class="node-preview__header" :style="{ background: nodeColor + '33' }">
            <i :class="plugin.icon" :style="{ color: nodeColor }"></i>
            <span>{{ label || plugin.label }}</span>
          </div>
          <div class="node-preview__body">
            <span class="text-xs text-slate-400">{{ plugin.description }}</span>
          </div>
        </div>
      </div>

      <!-- ── Label ──────────────────────────────────── -->
      <div class="field">
        <label class="field__label">اسم الـ Node</label>
        <prime_input_text v-model="label" :placeholder="plugin.label" class="w-full" />
      </div>

      <!-- ── Color ──────────────────────────────────── -->
      <div class="field">
        <label class="field__label">اللون</label>
        <div class="flex items-center gap-3">
          <input type="color" v-model="customColor" class="color-picker" />
          <div class="color-preview" :style="{ background: nodeColor }"></div>
          <prime_button label="Reset" size="small" text @click="customColor = plugin.color" />
        </div>
      </div>

      <!-- ── Dynamic Payload Fields ─────────────────── -->
      <!-- wait → seconds -->
      <div v-if="plugin.id === 'wait'" class="field">
        <label class="field__label">عدد الثواني</label>
        <prime_input_number
          v-model="formData.seconds"
          :min="0"
          :max="300"
          :step="0.5"
          show-buttons
          class="w-full"
        />
      </div>

      <!-- press → key -->
      <div v-else-if="plugin.id === 'press'" class="field">
        <label class="field__label">المفتاح</label>
        <prime_input_text
          v-model="formData.key"
          placeholder="Enter, Escape, Tab, F5..."
          class="w-full"
        />
      </div>

      <!-- hotkey → keys -->
      <div v-else-if="plugin.id === 'hotkey'" class="field">
        <label class="field__label">المفاتيح (مفصولة بـ +)</label>
        <prime_input_text
          :model-value="Array.isArray(formData.keys) ? formData.keys.join('+') : formData.keys"
          @update:model-value="formData.keys = $event.split('+').map((k) => k.trim())"
          placeholder="ctrl+shift+p"
          class="w-full"
        />
      </div>

      <!-- ai_action → prompt -->
      <div v-else-if="plugin.id === 'ai_action'" class="field">
        <label class="field__label">Prompt للـ AI</label>
        <prime_textarea
          v-model="formData.prompt"
          placeholder="اضغط على زرار Build في VSCode"
          rows="3"
          class="w-full"
        />
      </div>

      <!-- click_element → element_id (text input for now) -->
      <div v-else-if="plugin.id === 'click_element'" class="field">
        <label class="field__label">Element ID</label>
        <prime_input_text
          v-model="formData.element_id"
          placeholder="UUID بتاع الـ ProgramElement"
          class="w-full"
        />
        <small class="text-slate-400 text-xs">
          ملاحظة: هتقدر تختار من قائمة في الـ ActionPanel بعد الإضافة
        </small>
      </div>

      <!-- Error -->
      <div v-if="error" class="error-msg">
        <i class="pi pi-exclamation-triangle mr-2"></i>{{ error }}
      </div>
    </div>

    <!-- Footer -->
    <template #footer>
      <div class="flex justify-end gap-2">
        <prime_button
          label="إلغاء"
          severity="secondary"
          outlined
          @click="(emit('cancel'), emit('update:visible', false))"
        />
        <prime_button
          label="إضافة للـ Canvas"
          icon="pi pi-plus"
          :style="{ background: nodeColor, borderColor: nodeColor }"
          @click="handleConfirm"
        />
      </div>
    </template>
  </prime_dialog>
</template>

<style scoped>
.builder {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.builder__preview {
  display: flex;
  justify-content: center;
  padding: 16px 0;
}

.node-preview {
  width: 220px;
  border: 2px solid;
  border-radius: 10px;
  overflow: hidden;
  background: #1e293b;
}

.node-preview__header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  font-size: 0.85rem;
  font-weight: 600;
  color: #e2e8f0;
}

.node-preview__body {
  padding: 8px 12px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.field__label {
  font-size: 0.8rem;
  font-weight: 600;
  color: #94a3b8;
}

.color-picker {
  width: 40px;
  height: 32px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
}

.color-preview {
  width: 32px;
  height: 32px;
  border-radius: 6px;
}

.error-msg {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 6px;
  padding: 8px 12px;
  color: #f87171;
  font-size: 0.8rem;
}
</style>
