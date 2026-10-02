<script setup>
import { onMounted, ref } from 'vue'
import { listNotifications, markAllRead, markRead, archiveNotification } from '@/services/notifications'
const items = ref([]); const loading = ref(true)
const load = async () => { loading.value = true; try { items.value = await listNotifications() } finally { loading.value = false } }
const read = async (item) => { if (!item.read_at) { await markRead(item.id); item.read_at = new Date().toISOString() } }
const readAll = async () => { await markAllRead(); items.value.forEach(x => x.read_at = new Date().toISOString()) }
const archive = async (item) => { await archiveNotification(item.id); items.value = items.value.filter(x => x.id !== item.id) }
onMounted(load)
</script>
<template>
  <section class="space-y-5">
    <div class="flex items-center justify-between"><div><h1 class="text-2xl font-bold">Notifications</h1><p class="text-sm text-surface-500">System events from Tasks, Learning, Jobs, AI and Social.</p></div><button class="px-4 py-2 rounded-lg bg-primary text-white" @click="readAll">Mark all read</button></div>
    <div v-if="loading" class="p-8 text-center">Loading…</div>
    <div v-else-if="!items.length" class="p-10 rounded-2xl border border-dashed text-center text-surface-500">No notifications yet.</div>
    <div v-else class="space-y-2">
      <article v-for="item in items" :key="item.id" class="p-4 rounded-2xl border bg-white dark:bg-surface-900" :class="!item.read_at ? 'border-primary/40' : 'border-surface-200 dark:border-surface-800'">
        <div class="flex gap-3"><i class="pi pi-bell text-primary mt-1" /><div class="flex-1"><div class="flex justify-between gap-3"><h2 class="font-semibold">{{ item.title }}</h2><span class="text-xs text-surface-500">{{ new Date(item.created_at).toLocaleString() }}</span></div><p class="text-sm mt-1 text-surface-600 dark:text-surface-300">{{ item.message }}</p><div class="mt-3 flex gap-2"><button v-if="!item.read_at" class="text-xs px-3 py-1.5 rounded-lg bg-surface-100 dark:bg-surface-800" @click="read(item)">Mark read</button><button class="text-xs px-3 py-1.5 rounded-lg bg-surface-100 dark:bg-surface-800" @click="archive(item)">Archive</button></div></div></div>
      </article>
    </div>
  </section>
</template>
