<template>
  <aside class="sidebar" :class="{ collapsed }" aria-label="التنقل الرئيسي">
    <div class="brand">
      <div class="brand-mark" aria-hidden="true">✦</div>
      <div v-if="!collapsed" class="brand-copy">
        <strong>SO_IAM_OS</strong>
        <span>Personal AI OS</span>
      </div>
    </div>

    <button
      class="collapse-btn"
      type="button"
      @click="$emit('toggle')"
      :aria-label="collapsed ? 'فتح القائمة' : 'تصغير القائمة'"
      :title="collapsed ? 'فتح القائمة' : 'تصغير القائمة'"
    >
      {{ collapsed ? '→' : '←' }}
    </button>

    <nav class="nav">
      <div v-if="!collapsed" class="nav-label">مساحة العمل</div>
      <RouterLink
        v-for="item in mainItems"
        :key="item.path"
        :to="item.path"
        class="nav-item"
        active-class="active"
        @click="$emit('navigate')"
        :title="item.label"
        :aria-label="item.label"
      >
        <span class="nav-icon" aria-hidden="true">{{ item.icon }}</span>
        <span v-if="!collapsed">{{ item.label }}</span>
      </RouterLink>

      <div v-if="!collapsed" class="nav-label section-space">الأعمال والنمو</div>
      <RouterLink
        v-for="item in businessItems"
        :key="item.path"
        :to="item.path"
        class="nav-item"
        active-class="active"
        @click="$emit('navigate')"
        :title="item.label"
        :aria-label="item.label"
      >
        <span class="nav-icon" aria-hidden="true">{{ item.icon }}</span>
        <span v-if="!collapsed">{{ item.label }}</span>
      </RouterLink>

      <div v-if="!collapsed" class="nav-label section-space">النظام</div>
      <RouterLink
        v-for="item in secondaryItems"
        :key="item.path"
        :to="item.path"
        class="nav-item"
        active-class="active"
        @click="$emit('navigate')"
        :title="item.label"
        :aria-label="item.label"
      >
        <span class="nav-icon" aria-hidden="true">{{ item.icon }}</span>
        <span v-if="!collapsed">{{ item.label }}</span>
      </RouterLink>
    </nav>
  </aside>
</template>

<script setup>
import { RouterLink } from 'vue-router'

defineProps({ collapsed: Boolean })
defineEmits(['toggle', 'navigate'])

const mainItems = [
  { label: 'الرئيسية', icon: '⌂', path: '/' },
  { label: 'لوحة التحكم', icon: '◫', path: '/dashboard' },
  { label: 'الأهداف', icon: '◎', path: '/goals' },
  { label: 'المهام', icon: '✓', path: '/tasks' },
  { label: "Today's Tasks", icon: '◷', path: '/tasks/today' },
  { label: 'التعلم', icon: '◇', path: '/learning' },
  { label: 'موضوع التعلم', icon: '◈', path: '/learning/topics/1' },
  { label: 'المعرفة', icon: '▤', path: '/knowledge' },
  { label: 'الذاكرة', icon: '◉', path: '/memory' },
  { label: 'الوظائف', icon: '▣', path: '/jobs' },
  { label: 'المشروعات', icon: '◆', path: '/projects' },
  { label: 'التحديات', icon: '⚑', path: '/challenges' },
  { label: 'المالية', icon: '$', path: '/finance' },
  { label: 'المساعد الذكي', icon: '✦', path: '/ai' },
  { label: 'إعدادات الذكاء الاصطناعي', icon: '⚙', path: '/ai/control' },
  { label: 'عمليات ومراقبة AI', icon: '▥', path: '/ai/operations' },
  { label: 'مختبر أدوات AI', icon: '⚗', path: '/ai-tools' },
  { label: 'الأتمتة', icon: '⟳', path: '/automation' },
  { label: 'قائمة برامج الأتمتة', icon: '☰', path: '/automation_ProgramList' },
  { label: 'إنشاء برنامج أتمتة', icon: '＋', path: '/automation_programs_create' },
  { label: 'تعديل برنامج أتمتة', icon: '✎', path: '/automation/1' },
  { label: 'إنشاء مهمة أتمتة', icon: '⊕', path: '/automation_TaskCreate' },
  { label: 'محرر مهام الأتمتة', icon: '◧', path: '/automation_TaskEditor' },
]

const businessItems = [
  { label: 'الوكلاء', icon: '❖', path: '/agents' },
  { label: 'التحليلات', icon: '◔', path: '/analytics' },
  { label: 'البنية المعمارية', icon: '⬢', path: '/architecture' },
  { label: 'CRM', icon: '◳', path: '/crm' },
  { label: 'التسويق', icon: '📣', path: '/marketing' },
  { label: 'الإيرادات', icon: '📈', path: '/revenue' },
  { label: 'المبيعات', icon: '💼', path: '/sales' },
]

const secondaryItems = [
  { label: 'الملف الشخصي', icon: '☺', path: '/profile/me' },
  { label: 'التواصل الاجتماعي', icon: '◎', path: '/social' },
  { label: 'الإشعارات', icon: '♧', path: '/notifications' },
  { label: 'Scraper', icon: '⌕', path: '/scraper' },
  { label: 'Codex', icon: '⌘', path: '/codex' },
  { label: 'التقدم', icon: '↗', path: '/progress' },
  { label: 'وكلاء الذكاء الاصطناعي', icon: '✦', path: '/ai/agents' },
  { label: 'عن النظام', icon: 'ⓘ', path: '/About' },
  { label: 'الإعدادات', icon: '⚙', path: '/settings' },
  { label: 'هندسة الواجهة', icon: '✣', path: '/system/frontend' },
]
</script>
