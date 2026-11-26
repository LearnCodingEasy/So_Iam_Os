<script setup>
/*
===================================================
NodePluginCard.vue
src/components/Automation/Node/NodePluginCard.vue

المسؤولية: بطاقة عرض Plugin واحد في الـ NodeMarketplace
✅ Draggable — المستخدم يسحبها على الـ Canvas
✅ تعرض: icon, label, description, category, badges

الاستخدام:
<NodePluginCard
  :plugin="plugin"
  @dragstart="onDragStart"
  @add-to-canvas="onAddToCanvas"
/>
===================================================

*/
const props = defineProps({
  plugin: {
    type: Object,
    required: true,
    // {
    //   id, label, icon, color, description,
    //   category, meta: { isPremium, isExperimental }
    // }
  },
  dragging: { type: Boolean, default: false },
})

const emit = defineEmits([
  'dragstart', // يبدأ السحب — يرجع plugin object
  'add-to-canvas', // ضغط "Add" — للـ canvas مباشرة بدون drag
])

const onDragStart = (e) => {
  e.dataTransfer.effectAllowed = 'copy'
  emit('dragstart', props.plugin)
}
</script>

<template>
  <div
    class="plugin-card"
    :class="{ 'plugin-card--dragging': dragging }"
    draggable="true"
    @dragstart="onDragStart"
    :title="`اسحب ${plugin.label} على الـ Canvas`"
  >
    <!-- Icon Area -->
    <div
      class="plugin-card__icon"
      :style="{ background: plugin.color + '22', borderColor: plugin.color + '55' }"
    >
      <i :class="plugin.icon" :style="{ color: plugin.color, fontSize: '1.2rem' }"></i>
    </div>

    <!-- Info -->
    <div class="plugin-card__info">
      <div class="plugin-card__title-row">
        <span class="plugin-card__label">{{ plugin.label }}</span>

        <!-- Badges -->
        <prime_tag
          v-if="plugin.meta?.isExperimental"
          value="Beta"
          severity="warning"
          class="!text-xs !px-1 !py-0"
        />
        <prime_tag
          v-if="plugin.meta?.isPremium"
          value="Pro"
          severity="info"
          class="!text-xs !px-1 !py-0"
        />
      </div>

      <p class="plugin-card__desc">{{ plugin.description }}</p>
    </div>

    <!-- Add Button -->
    <prime_button
      icon="pi pi-plus"
      size="small"
      rounded
      outlined
      :style="{ color: plugin.color, borderColor: plugin.color + '88' }"
      class="plugin-card__add-btn"
      @click.stop="emit('add-to-canvas', plugin)"
      v-tooltip.left="'أضف للـ Canvas plagin'"
    />
  </div>
</template>

<style scoped>
.plugin-card {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  background: #1e293b;
  border: 1px solid #334155;
  border-radius: 10px;
  cursor: grab;
  transition: all 0.15s ease;
  user-select: none;
}

.plugin-card:hover {
  border-color: #475569;
  background: #263348;
  transform: translateX(-2px);
}

.plugin-card--dragging {
  opacity: 0.5;
  cursor: grabbing;
}

.plugin-card__icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  border: 1px solid;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.plugin-card__info {
  flex: 1;
  min-width: 0;
}

.plugin-card__title-row {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 2px;
}

.plugin-card__label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #e2e8f0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.plugin-card__desc {
  font-size: 0.72rem;
  color: #64748b;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin: 0;
}

.plugin-card__add-btn {
  flex-shrink: 0;
  opacity: 0;
  transition: opacity 0.15s;
}

.plugin-card:hover .plugin-card__add-btn {
  opacity: 1;
}
</style>
