<template>
  <aside class="sidebar" :class="{ collapsed }">
    <div class="brand">
      <div class="brand-mark">✦</div>
      <div v-if="!collapsed" class="brand-copy">
        <strong>Opportunity AI</strong>
        <span>AI Career Engine</span>
      </div>
    </div>

    <button class="collapse-btn" @click="$emit('toggle')" :title="collapsed ? 'فتح القائمة' : 'تصغير القائمة'">
      {{ collapsed ? "→" : "←" }}
    </button>

    <nav class="nav">
      <div v-if="!collapsed" class="nav-label">الرئيسية</div>

      <a
        v-for="item in mainItems"
        :key="item.label"
        href="#"
        class="nav-item"
        :class="{ active: item.active }"
        @click.prevent
        :title="item.label"
      >
        <span class="nav-icon">{{ item.icon }}</span>
        <span v-if="!collapsed">{{ item.label }}</span>
        <span v-if="item.badge && !collapsed" class="nav-badge">{{ item.badge }}</span>
      </a>

      <div v-if="!collapsed" class="nav-label section-space">إدارة النظام</div>

      <a
        v-for="item in secondaryItems"
        :key="item.label"
        href="#"
        class="nav-item"
        @click.prevent
        :title="item.label"
      >
        <span class="nav-icon">{{ item.icon }}</span>
        <span v-if="!collapsed">{{ item.label }}</span>
      </a>
    </nav>

    <div class="sidebar-bottom">
      <div class="user-card">
        <div class="avatar">ح</div>
        <div v-if="!collapsed" class="user-copy">
          <strong>حسام رشاد</strong>
          <span>Developer</span>
        </div>
        <button v-if="!collapsed" class="more-btn">•••</button>
      </div>
    </div>
  </aside>
</template>

<script setup>
defineProps({
  collapsed: Boolean,
});

defineEmits(["toggle"]);

const mainItems = [
  { label: "لوحة التحكم", icon: "⌂", active: true },
  { label: "الفرص", icon: "◈", badge: "24" },
  { label: "الوظائف", icon: "▣" },
  { label: "المشاريع", icon: "◆" },
  { label: "طلبات التقديم", icon: "✓" },
  { label: "المهارات", icon: "◇" },
  { label: "المساعد الذكي", icon: "✦" },
];

const secondaryItems = [
  { label: "التحليلات", icon: "◌" },
  { label: "الإعدادات", icon: "⚙" },
];
</script>
