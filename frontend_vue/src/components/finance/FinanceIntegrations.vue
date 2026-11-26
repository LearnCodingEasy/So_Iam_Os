<template>
  <section class="section-grid">
    <Card class="panel wide">
      <template #title> SO_IAM_OS Ecosystem Integration </template>

      <template #content>
        <div class="integration-grid">
          <div v-for="(item, key) in ecosystem.connections || {}" :key="key" class="integration">
            <Tag
              :value="item.available ? 'CONNECTED' : 'UNAVAILABLE'"
              :severity="item.available ? 'success' : 'danger'"
            />

            <strong>{{ key }}</strong>

            <span> {{ item.count ?? 0 }} records </span>
          </div>
        </div>
      </template>
    </Card>

    <Card class="panel">
      <template #title> Finance Flow </template>

      <template #content>
        <ul class="flow-list">
          <li v-for="item in ecosystem.recommended_flow || []" :key="item">
            {{ item }}
          </li>
        </ul>

        <div class="opportunity">
          <strong>
            {{ ecosystem.income_opportunities || 0 }}
          </strong>

          <span> فرصة دخل/توصية وظيفية </span>
        </div>
      </template>
    </Card>
  </section>
</template>

<script setup>
import Card from 'primevue/card'
import Tag from 'primevue/tag'

defineProps({
  ecosystem: {
    type: Object,
    default: () => ({
      connections: {},
      recommended_flow: [],
      income_opportunities: 0,
    }),
  },
})
</script>
