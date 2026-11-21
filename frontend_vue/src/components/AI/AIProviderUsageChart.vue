<template><div class="usage-chart"><Bar :data="data" :options="options" /></div></template>
<script setup>
import { computed } from 'vue'
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Tooltip, Legend } from 'chart.js'
ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend)
const props = defineProps({ rows: { type: Array, default: () => [] } })
const data = computed(() => ({ labels: props.rows.map((row) => row.provider), datasets: [{ label: 'Messages', data: props.rows.map((row) => row.count || 0), borderWidth: 1 }] }))
const options = { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } }
</script>
<style scoped>.usage-chart{height:280px}</style>
