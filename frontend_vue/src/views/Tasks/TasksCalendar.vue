<script setup>
import { computed, onMounted, ref } from 'vue'
import { listTasks, createTask, updateTask, completeTask } from '@/services/tasks'
import api from '@/services/api'
import { endpoints } from '@/services/endpoints'
const cursor = ref(new Date()); const view = ref('week'); const tasks = ref([]); const loading = ref(false)
const startOfWeek = (date) => { const d = new Date(date); const day = d.getDay(); d.setDate(d.getDate() - day); d.setHours(0,0,0,0); return d }
const rangeStart = computed(() => view.value === 'month' ? new Date(cursor.value.getFullYear(), cursor.value.getMonth(), 1) : startOfWeek(cursor.value))
const rangeEnd = computed(() => view.value === 'month' ? new Date(cursor.value.getFullYear(), cursor.value.getMonth()+1, 0) : new Date(rangeStart.value.getTime()+6*86400000))
const days = computed(() => { const arr=[]; const count=view.value==='month'?rangeEnd.value.getDate():7; const base=view.value==='month'?rangeStart.value:startOfWeek(cursor.value); for(let i=0;i<count;i++){const d=new Date(base);d.setDate(base.getDate()+i);arr.push(d)} return arr })
const key = d => d.toISOString().slice(0,10)
const load = async () => { loading.value=true; try { const r=await api.get(endpoints.tasks.calendar,{params:{start:key(rangeStart.value),end:key(rangeEnd.value)}}); tasks.value=r.data.results || r.data || [] } finally { loading.value=false } }
const prev = () => { const d=new Date(cursor.value); if(view.value==='month') d.setMonth(d.getMonth()-1); else d.setDate(d.getDate()-7); cursor.value=d; load() }
const next = () => { const d=new Date(cursor.value); if(view.value==='month') d.setMonth(d.getMonth()+1); else d.setDate(d.getDate()+7); cursor.value=d; load() }
const today = () => { cursor.value=new Date(); load() }
const byDay = d => tasks.value.filter(t => { const start=t.start_at ? t.start_at.slice(0,10) : t.scheduled_date; const end=t.end_at ? t.end_at.slice(0,10) : start; return start <= key(d) && end >= key(d) })
const addQuickTask = async d => { const title=window.prompt('Task title'); if(!title) return; const task=await createTask({title,scheduled_date:key(d),start_at:`${key(d)}T09:00:00`,end_at:`${key(d)}T10:00:00`}); tasks.value.push(task) }
const toggle = async task => { if(task.status==='completed') return; const updated=await completeTask(task.id,{actual_minutes:task.estimated_minutes}); Object.assign(task,updated) }
onMounted(load)
</script>
<template>
  <section class="space-y-4"><div class="flex flex-wrap items-center gap-3"><div><h1 class="text-2xl font-bold">Tasks Calendar</h1><p class="text-sm text-surface-500">Plan goals, learning and career work across days.</p></div><div class="flex-1"/><button class="px-3 py-2 rounded-lg border" @click="today">Today</button><button class="px-2 py-2 rounded-lg border" @click="prev">‹</button><button class="px-2 py-2 rounded-lg border" @click="next">›</button><select v-model="view" class="px-3 py-2 rounded-lg border" @change="load"><option value="week">Week</option><option value="month">Month</option></select></div>
    <div class="rounded-2xl border overflow-hidden bg-white dark:bg-surface-900"><div class="grid" :style="{gridTemplateColumns:`repeat(${days.length}, minmax(0,1fr))`}"><div v-for="day in days" :key="key(day)" class="min-h-36 border-r border-b last:border-r-0 p-2 cursor-pointer hover:bg-surface-50 dark:hover:bg-surface-800" @dblclick="addQuickTask(day)"><div class="text-xs font-semibold" :class="key(day)===key(new Date())?'text-primary':''">{{ day.toLocaleDateString(undefined,{weekday:'short',month:'short',day:'numeric'}) }}</div><div class="mt-2 space-y-1"><div v-for="task in byDay(day)" :key="task.id" class="text-xs p-2 rounded-lg bg-primary/10 border border-primary/20" :class="task.status==='completed'?'opacity-50 line-through':''"><div class="font-medium">{{ task.title }}</div><button v-if="task.status!=='completed'" class="text-[10px] mt-1 underline" @click.stop="toggle(task)">Complete</button></div></div></div></div></div>
    <div v-if="loading" class="text-sm text-surface-500">Loading calendar…</div><p class="text-xs text-surface-500">Tip: double-click a day to create a task. Multi-day tasks span every day between start and end.</p>
  </section>
</template>
