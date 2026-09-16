<template>
  <header class="topbar">
    <div class="topbar-start">
      <button class="mobile-menu" @click="$emit('toggle-sidebar')">☰</button>
      <div>
        <h1>لوحة التحكم</h1>
        <p>نظرة سريعة على فرصك وأداء النظام</p>
      </div>
    </div>

    <div class="topbar-actions">
      <label class="search">
        <span>⌕</span>
        <input placeholder="ابحث عن فرصة، شركة..." />
        <kbd>⌘ K</kbd>
      </label>

      <button class="icon-btn" title="الإشعارات">
        ♧
        <span class="notification-dot">3</span>
      </button>

      <button class="icon-btn" title="الوضع الليلي">☾</button>
    </div>
  </header>
</template>

<script setup>
defineEmits(["toggle-sidebar"]);
</script>
