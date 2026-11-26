<script setup>
// ============================================================
//  NodeMarketplace.vue
//  src/components/Automation/Node/NodeMarketplace.vue
//
//  المسؤولية:
//   - يعرض كل الـ plugins المتاحة (من PluginRegistry)
//   - يعرض programs + program elements كـ draggable items
//   - بيحل محل الـ aside القديمة في AutomationView
//
//  الاستخدام في AutomationView:
//    <NodeMarketplace
//      :programs="programs"
//      :elements="programsElement"
//      :delays="delays"
//      :tasks="tasks"
//      @drag-start="startDrag"
//      @item-click="onItemClick"
//    />
//
//  الـ emit: @drag-start → { type, id }
//  مثال: { type: 'program', id: 'vscode-uuid' }
//        { type: 'program-element', id: 'btn-uuid' }
//        { type: 'plugin', id: 'wait' }  ← من PluginRegistry
// ============================================================
import { ref, computed } from 'vue'
import registry, { PLUGIN_CATEGORIES } from '@/plugins/PluginRegistry'
import NodePluginCard from './NodePluginCard.vue'

const props = defineProps({
  programs: { type: Array, default: () => [] },
  elements: { type: Array, default: () => [] },
  delays: { type: Array, default: () => [] },
  tasks: { type: Array, default: () => [] },
  workflows: { type: Array, default: () => [] },
  loadingPrograms: { type: Boolean, default: false },
  loadingElements: { type: Boolean, default: false },
  loadingTasks: { type: Boolean, default: false },
})

const emit = defineEmits([
  'drag-start', // المستخدم بدأ السحب — { type, id }
  'item-click', // المستخدم ضغط على item — { type, id }
  'create-program', // ضغط ➕ Programs
  'create-element', // ضغط ➕ Elements
  'create-task', // ضغط ➕ Tasks
  'edit-program', // ضغط ✏️
  'delete-program', // ضغط 🗑️
  'edit-element',
  'delete-element',
  'edit-task',
  'delete-task',
  'select-workflow',
])

// ─── Tab & Search ─────────────────────────────────────────
const activeTab = ref(0) // 0=Programs, 1=Elements, 2=Plugins, 3=Tasks, 4=Workflows
const searchText = ref('')
const activeCategory = ref('all') // all | programs | input | timing | ai

// ─── Plugins from Registry ────────────────────────────────
const allPlugins = computed(() => registry.getMarketplaceItems())

const filteredPlugins = computed(() => {
  let list = allPlugins.value
  if (activeCategory.value !== 'all') {
    list = list.filter((p) => p.category === activeCategory.value)
  }
  if (searchText.value.trim()) {
    const q = searchText.value.toLowerCase()
    list = list.filter(
      (p) =>
        p.label.toLowerCase().includes(q) ||
        p.description.toLowerCase().includes(q) ||
        p.tags?.some((t) => t.includes(q)),
    )
  }
  return list
})

// ─── Filtered Programs/Elements ───────────────────────────
const filteredPrograms = computed(() => {
  if (!searchText.value.trim()) return props.programs
  const q = searchText.value.toLowerCase()
  return props.programs.filter((p) => p.name?.toLowerCase().includes(q))
})

const filteredElements = computed(() => {
  if (!searchText.value.trim()) return props.elements
  const q = searchText.value.toLowerCase()
  return props.elements.filter((e) => e.name?.toLowerCase().includes(q))
})

// ─── Drag Handlers ────────────────────────────────────────
const draggingId = ref(null)

const onDragStart = (type, id) => {
  draggingId.value = id
  emit('drag-start', { type, id })
}

const onDragEnd = () => {
  draggingId.value = null
}

const onPluginDragStart = (plugin) => {
  draggingId.value = plugin.id
  emit('drag-start', { type: 'plugin', id: plugin.id })
}

// ─── Category Tabs ────────────────────────────────────────
const categories = computed(() => [
  { key: 'all', label: 'الكل' },
  ...Object.entries(PLUGIN_CATEGORIES).map(([key, val]) => ({
    key,
    label: val.label,
    icon: val.icon,
  })),
])

// ─── Tabs Config ──────────────────────────────────────────
const tabs = [
  { key: 'workflows', label: 'Workflows', icon: 'pi pi-sitemap' },
  { key: 'programs', label: 'Programs', icon: 'pi pi-desktop' },
  { key: 'elements', label: 'Elements', icon: 'pi pi-th-large' },
  { key: 'actions', label: 'Actions', icon: 'pi pi-bolt' },
  { key: 'tasks', label: 'Tasks', icon: 'pi pi-list' },
]
</script>

<template>
  <div class="marketplace">
    <!-- ── Search ─────────────────────────────── -->
    <div class="marketplace__search">
      <prime_icon_field>
        <prime_input_icon class="pi pi-search" />
        <prime_input_text v-model="searchText" placeholder="ابحث..." size="small" class="w-full" />
      </prime_icon_field>
    </div>
    <div class="wrapper_control">
      <!-- ── Tabs ────────────────────────────── -->
      <div class="marketplace__tabs">
        <button
          v-for="(tab, i) in tabs"
          :key="tab.key"
          class="tab-btn"
          :class="{ 'tab-btn--active': activeTab === i }"
          @click="activeTab = i"
          :title="tab.label"
        >
          <i :class="tab.icon"></i>
          <span class="tab-btn__label">{{ tab.label }}</span>
        </button>
      </div>

      <!-- ── Content ─────────────────────────── -->
      <div class="marketplace__content">
        <!-- ⑤ Workflows Tab ───────────────────── -->
        <template v-if="activeTab === 0">
          <div class="section-header">
            <span>⚡ Workflows</span>
          </div>

          <div
            v-for="w in workflows"
            :key="w.id"
            class="item-card item-card--workflow"
            @click="emit('select-workflow', w.id)"
          >
            <i class="pi pi-sitemap item-card__icon" style="color: #f59e0b"></i>
            <div class="item-card__info">
              <span class="item-card__name">{{ w.name }}</span>
              <prime_tag
                :value="w.status"
                :severity="
                  w.status === 'active'
                    ? 'success'
                    : w.status === 'paused'
                      ? 'warning'
                      : 'secondary'
                "
                class="!text-xs"
              />
            </div>
          </div>
        </template>
        <!-- ① Programs Tab ───────────────────── -->
        <template v-else-if="activeTab === 1">
          <div class="section-header">
            <span>🖥️ Programs</span>
            <prime_button
              icon="pi pi-plus"
              size="small"
              text
              rounded
              @click="emit('create-program')"
              v-tooltip.left="'إضافة برنامج جديد'"
            />
          </div>

          <div v-if="loadingPrograms" class="skeleton-list">
            <prime_skeleton v-for="i in 3" :key="i" height="52px" borderRadius="8px" />
          </div>

          <div v-else-if="!filteredPrograms.length" class="empty-hint">
            لا يوجد برامج — اضغط ➕ لإضافة أول برنامج
          </div>

          <div
            v-for="p in filteredPrograms"
            :key="p.id"
            class="item-card"
            draggable="true"
            @dragstart="onDragStart('program', p.id)"
            @dragend="onDragEnd"
            @click="emit('item-click', { type: 'program', id: p.id })"
          >
            <img v-if="p.get_image" :src="p.get_image" :alt="p.name" class="item-card__img" />
            <i v-else class="pi pi-desktop item-card__icon" style="color: #16a34a"></i>
            <span class="item-card__name">{{ p.name }}</span>
            <div class="item-card__actions">
              <prime_button
                icon="pi pi-pencil"
                size="small"
                text
                rounded
                @click.stop="emit('edit-program', p.id)"
              />
              <prime_button
                icon="pi pi-trash"
                size="small"
                text
                rounded
                severity="danger"
                @click.stop="emit('delete-program', p)"
              />
            </div>
          </div>
        </template>

        <!-- ② Elements Tab ────────────────────── -->
        <template v-else-if="activeTab === 2">
          <div class="section-header">
            <span>🧩 Elements</span>
            <prime_button
              icon="pi pi-plus"
              size="small"
              text
              rounded
              @click="emit('create-element')"
            />
          </div>

          <div v-if="loadingElements" class="skeleton-list">
            <prime_skeleton v-for="i in 3" :key="i" height="52px" borderRadius="8px" />
          </div>

          <div v-else-if="!filteredElements.length" class="empty-hint">لا يوجد عناصر</div>

          <div
            v-for="el in filteredElements"
            :key="el.id"
            class="item-card"
            draggable="true"
            @dragstart="onDragStart('program-element', el.id)"
            @dragend="onDragEnd"
            @click="emit('item-click', { type: 'program-element', id: el.id })"
          >
            <img v-if="el.get_image" :src="el.get_image" :alt="el.name" class="item-card__img" />
            <i v-else class="pi pi-th-large item-card__icon" style="color: #0ea5e9"></i>
            <div class="item-card__info">
              <span class="item-card__name">{{ el.name }}</span>
              <span class="item-card__meta">{{ el.selector_type }}</span>
            </div>
            <div class="item-card__actions">
              <prime_button
                icon="pi pi-pencil"
                size="small"
                text
                rounded
                @click.stop="emit('edit-element', el.id)"
              />
              <prime_button
                icon="pi pi-trash"
                size="small"
                text
                rounded
                severity="danger"
                @click.stop="emit('delete-element', el)"
              />
            </div>
          </div>
        </template>

        <!-- ③ Actions/Plugins Tab ─────────────── -->
        <template v-else-if="activeTab === 3">
          <!-- Category Filter -->
          <div class="category-filter">
            <button
              v-for="cat in categories"
              :key="cat.key"
              class="cat-btn"
              :class="{ 'cat-btn--active': activeCategory === cat.key }"
              @click="activeCategory = cat.key"
            >
              {{ cat.label }}
            </button>
          </div>

          <div v-if="!filteredPlugins.length" class="empty-hint">لا يوجد نتائج</div>

          <NodePluginCard
            v-for="plugin in filteredPlugins"
            :key="plugin.id"
            :plugin="plugin"
            :dragging="draggingId === plugin.id"
            @dragstart="onPluginDragStart"
            @add-to-canvas="emit('drag-start', { type: 'plugin', id: $event.id })"
          />
        </template>

        <!-- ④ Tasks Tab ───────────────────────── -->
        <template v-else-if="activeTab === 4">
          <div class="section-header">
            <span>📋 Tasks</span>
            <prime_button
              icon="pi pi-plus"
              size="small"
              text
              rounded
              @click="emit('create-task')"
            />
          </div>

          <div
            v-for="t in tasks"
            :key="t.id"
            class="item-card"
            draggable="true"
            @dragstart="onDragStart('task', t.id)"
            @dragend="onDragEnd"
            @click="emit('item-click', { type: 'task', id: t.id })"
          >
            <i class="pi pi-list item-card__icon" style="color: #8b5cf6"></i>
            <span class="item-card__name">{{ t.name }}</span>
            <div class="item-card__actions">
              <prime_button
                icon="pi pi-pencil"
                size="small"
                text
                rounded
                @click.stop="emit('edit-task', t.id)"
              />
              <prime_button
                icon="pi pi-trash"
                size="small"
                text
                rounded
                severity="danger"
                @click.stop="emit('delete-task', t)"
              />
            </div>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.marketplace {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: #0f172a;
  border-right: 1px solid #1e293b;

  .marketplace__search {
    padding: 10px 10px 0;
  }
  .wrapper_control {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(60px, 1fr));
    height: 100vh;
    .marketplace__tabs {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: space-between;
      gap: 2px;
      padding: 8px 8px 0;
      border-bottom: 1px solid #1e293b;
      border: 0.2rem solid rgb(192, 191, 191);
      height: calc(100vh - 45px);
      .tab-btn {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 2px;
        padding: 6px 8px;
        border-radius: 6px 6px 0 0;
        border: none;
        background: transparent;
        color: #64748b;
        cursor: pointer;
        font-size: 0.65rem;
        transition: all 0.15s;
        flex: 1;
        &:hover {
          background: #1e293b;
          color: #94a3b8;
        }
        &.tab-btn--active {
          background: #1e293b;
          color: #60a5fa;
          border-bottom: 2px solid #60a5fa;
        }
        &.tab-btn__label {
          font-size: 0.6rem;
          white-space: nowrap;
        }
        i {
          font-size: 0.9rem;
        }
      }
    }
    .marketplace__content {
      grid-column: span 4;
      grid-row: span 6;
      flex: 1;
      overflow-y: auto;
      padding: 8px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
  }
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 0.75rem;
  font-weight: 600;
  color: #94a3b8;
  padding: 4px 2px;
}

.item-card {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 10px;
  background: #1e293b;
  border: 1px solid #334155;
  border-radius: 8px;
  cursor: grab;
  transition: all 0.15s;
}

.item-card:hover {
  border-color: #475569;
  background: #263348;
}
.item-card--workflow {
  cursor: pointer;
}

.item-card__img {
  width: 28px;
  height: 28px;
  border-radius: 6px;
  object-fit: cover;
  flex-shrink: 0;
}

.item-card__icon {
  font-size: 1rem;
  flex-shrink: 0;
}

.item-card__info {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 0;
}

.item-card__name {
  font-size: 0.8rem;
  color: #e2e8f0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex: 1;
}

.item-card__meta {
  font-size: 0.65rem;
  color: #64748b;
}

.item-card__actions {
  display: flex;
  gap: 2px;
  opacity: 0;
  transition: opacity 0.15s;
}

.item-card:hover .item-card__actions {
  opacity: 1;
}

.empty-hint {
  text-align: center;
  color: #475569;
  font-size: 0.75rem;
  padding: 24px 8px;
}

.skeleton-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.category-filter {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  padding: 4px 0 8px;
}

.cat-btn {
  padding: 3px 8px;
  border-radius: 20px;
  border: 1px solid #334155;
  background: transparent;
  color: #64748b;
  font-size: 0.7rem;
  cursor: pointer;
  transition: all 0.15s;
}

.cat-btn:hover {
  border-color: #475569;
  color: #94a3b8;
}
.cat-btn--active {
  background: #1d4ed8;
  border-color: #1d4ed8;
  color: white;
}
</style>
