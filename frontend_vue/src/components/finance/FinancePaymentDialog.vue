<template>
  <Dialog
    :visible="visible"
    modal
    header="تسجيل دفعة"
    :style="{ width: 'min(460px, 94vw)' }"
    @update:visible="$emit('update:visible', $event)"
  >
    <div class="form-grid">
      <div class="field">
        <label>المبلغ</label>

        <InputNumber v-model="localForm.amount" :min="0" class="w-full" />
      </div>

      <div class="field">
        <label>التاريخ</label>

        <DatePicker v-model="localForm.paid_on" dateFormat="yy-mm-dd" showIcon class="w-full" />
      </div>

      <div class="field full">
        <label>ملاحظة</label>

        <InputText v-model="localForm.note" class="w-full" />
      </div>
    </div>

    <template #footer>
      <Button label="إلغاء" text @click="$emit('cancel')" />

      <Button label="تسجيل" icon="pi pi-check" :loading="saving" @click="$emit('save')" />
    </template>
  </Dialog>
</template>

<script setup>
import { ref, watch } from 'vue'

import Dialog from 'primevue/dialog'
import Button from 'primevue/button'
import InputNumber from 'primevue/inputnumber'
import InputText from 'primevue/inputtext'
import DatePicker from 'primevue/datepicker'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false,
  },

  paymentForm: {
    type: Object,
    default: () => ({
      amount: 0,
      paid_on: new Date(),
      note: '',
    }),
  },

  saving: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['update:visible', 'update:paymentForm', 'cancel', 'save'])

const localForm = ref({
  ...props.paymentForm,
})

watch(
  () => props.paymentForm,
  (value) => {
    localForm.value = {
      ...value,
    }
  },
  {
    deep: true,
    immediate: true,
  },
)

watch(
  localForm,
  (value) => {
    emit('update:paymentForm', {
      ...value,
    })
  },
  {
    deep: true,
  },
)
</script>
