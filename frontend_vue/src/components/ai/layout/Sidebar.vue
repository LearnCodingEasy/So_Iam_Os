<template>
  <aside ref="rootEl" class="sidebar" :class="{ collapsed }" aria-label="التنقل الرئيسي">
    <div class="brand">
      <div class="brand-mark" aria-hidden="true"><i class="pi pi-sparkles" /></div>
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
      <i
        :class="collapsed ? 'pi pi-angle-double-left' : 'pi pi-angle-double-right'"
        aria-hidden="true"
      />
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
        <i class="nav-icon" :class="item.icon" aria-hidden="true" />
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
        <i class="nav-icon" :class="item.icon" aria-hidden="true" />
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
        <i class="nav-icon" :class="item.icon" aria-hidden="true" />
        <span v-if="!collapsed">{{ item.label }}</span>
      </RouterLink>
    </nav>
  </aside>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { gsap, prefersReducedMotion } from '@/composables/useMotion'

defineProps({ collapsed: Boolean })
defineEmits(['toggle', 'navigate'])

// Entrance: brand + nav items stagger in once. Context is reverted on unmount (no leaked tweens).
const rootEl = ref(null)
let ctx = null
onMounted(() => {
  if (prefersReducedMotion() || !rootEl.value) return
  ctx = gsap.context(() => {
    gsap.from('.brand, .nav-item', {
      opacity: 0,
      x: 14,
      duration: 0.4,
      stagger: 0.018,
      ease: 'power2.out',
      clearProps: 'opacity,transform',
    })
  }, rootEl.value)
})
onBeforeUnmount(() => ctx?.revert())

const mainItems = [
  { label: 'الرئيسية', icon: 'pi pi-home', path: '/' },
  { label: 'لوحة التحكم', icon: 'pi pi-th-large', path: '/dashboard' },
  { label: 'الأهداف', icon: 'pi pi-bullseye', path: '/goals' },
  { label: 'المهام', icon: 'pi pi-check-square', path: '/tasks' },
  { label: "Today's Tasks", icon: 'pi pi-clock', path: '/tasks/today' },
  { label: 'التعلم', icon: 'pi pi-book', path: '/learning' },
  { label: 'موضوع التعلم', icon: 'pi pi-bookmark', path: '/learning/topics/1' },
  { label: 'المعرفة', icon: 'pi pi-database', path: '/knowledge' },
  { label: 'الذاكرة', icon: 'pi pi-history', path: '/memory' },
  { label: 'الوظائف', icon: 'pi pi-briefcase', path: '/jobs' },
  { label: 'المشروعات', icon: 'pi pi-folder-open', path: '/projects' },
  { label: 'التحديات', icon: 'pi pi-flag', path: '/challenges' },
  { label: 'المالية', icon: 'pi pi-wallet', path: '/finance' },
  { label: 'المساعد الذكي', icon: 'pi pi-sparkles', path: '/ai' },
  { label: 'إعدادات الذكاء الاصطناعي', icon: 'pi pi-sliders-h', path: '/ai/control' },
  { label: 'عمليات ومراقبة AI', icon: 'pi pi-chart-bar', path: '/ai/operations' },
  { label: 'مختبر أدوات AI', icon: 'pi pi-wrench', path: '/ai-tools' },
  { label: 'الأتمتة', icon: 'pi pi-sync', path: '/automation' },
  { label: 'قائمة برامج الأتمتة', icon: 'pi pi-list', path: '/automation_ProgramList' },
  { label: 'إنشاء برنامج أتمتة', icon: 'pi pi-plus-circle', path: '/automation_programs_create' },
  { label: 'تعديل برنامج أتمتة', icon: 'pi pi-pencil', path: '/automation/1' },
  { label: 'إنشاء مهمة أتمتة', icon: 'pi pi-plus', path: '/automation_TaskCreate' },
  { label: 'محرر مهام الأتمتة', icon: 'pi pi-file-edit', path: '/automation_TaskEditor' },
]

const businessItems = [
  { label: 'الوكلاء', icon: 'pi pi-users', path: '/agents' },
  { label: 'التحليلات', icon: 'pi pi-chart-line', path: '/analytics' },
  { label: 'البنية المعمارية', icon: 'pi pi-sitemap', path: '/architecture' },
  { label: 'CRM', icon: 'pi pi-id-card', path: '/crm' },
  { label: 'التسويق', icon: 'pi pi-megaphone', path: '/marketing' },
  { label: 'الإيرادات', icon: 'pi pi-dollar', path: '/revenue' },
  { label: 'المبيعات', icon: 'pi pi-shopping-cart', path: '/sales' },
]

const secondaryItems = [
  { label: 'الملف الشخصي', icon: 'pi pi-user', path: '/profile/me' },
  { label: 'التواصل الاجتماعي', icon: 'pi pi-comments', path: '/social' },
  { label: 'الإشعارات', icon: 'pi pi-bell', path: '/notifications' },
  { label: 'Scraper', icon: 'pi pi-search', path: '/scraper' },
  { label: 'Codex', icon: 'pi pi-code', path: '/codex' },
  { label: 'التقدم', icon: 'pi pi-chart-line', path: '/progress' },
  { label: 'وكلاء الذكاء الاصطناعي', icon: 'pi pi-microchip-ai', path: '/ai/agents' },
  { label: 'عن النظام', icon: 'pi pi-info-circle', path: '/About' },
  { label: 'الإعدادات', icon: 'pi pi-cog', path: '/settings' },
  { label: 'هندسة الواجهة', icon: 'pi pi-desktop', path: '/system/frontend' },
]
</script>
