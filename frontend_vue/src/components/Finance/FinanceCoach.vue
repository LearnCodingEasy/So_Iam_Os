<template>
  <section class="section-grid">
    <Card class="panel wide">
      <template #title> AI Financial Coach 🤖 </template>

      <template #content>
        <Textarea
          :modelValue="question"
          rows="5"
          class="w-full"
          placeholder="مثال: لو وفرت 500 شهريًا أوصل لهدفي إمتى؟"
          @update:modelValue="$emit('update:question', $event)"
        />

        <Button
          class="w-full coach-button"
          label="اسأل"
          icon="pi pi-send"
          :loading="loading"
          @click="$emit('ask')"
        />

        <div v-if="answer" class="coach-answer">
          {{ answer }}
        </div>
      </template>
    </Card>

    <Card class="panel">
      <template #title> مبدأ الـ AI </template>

      <template #content>
        <p class="muted">
          الـ AI يستخدم البيانات المالية المتاحة ويقدم تحليلًا وتقديرات وسيناريوهات. القرار النهائي
          يظل للمستخدم.
        </p>
      </template>
    </Card>
  </section>
</template>

<script setup>
import Card from 'primevue/card'
import Button from 'primevue/button'
import Textarea from 'primevue/textarea'

defineProps({
  question: {
    type: String,
    default: '',
  },

  answer: {
    type: String,
    default: '',
  },

  loading: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['update:question', 'ask'])
</script>
