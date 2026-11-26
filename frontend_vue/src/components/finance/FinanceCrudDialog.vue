<template>
  <Dialog
    :visible="visible"
    modal
    :header="formTitle"
    :style="{ width: 'min(720px, 94vw)' }"
    @update:visible="$emit('update:visible', $event)"
  >
    <div class="form-grid">
      <!-- Transaction -->
      <template v-if="formType === 'transaction'">
        <div class="field full">
          <label>الوصف</label>
          <InputText v-model="localForm.description" class="w-full" />
        </div>

        <div class="field">
          <label>النوع</label>

          <Select
            v-model="localForm.kind"
            :options="[
              { label: 'دخل', value: 'income' },
              { label: 'مصروف', value: 'expense' },
              { label: 'ادخار', value: 'saving' },
              { label: 'سداد دين', value: 'debt_payment' },
            ]"
            optionLabel="label"
            optionValue="value"
            class="w-full"
          />
        </div>

        <div class="field">
          <label>المبلغ</label>

          <InputNumber
            v-model="localForm.amount"
            :min="0"
            mode="decimal"
            :minFractionDigits="2"
            class="w-full"
          />
        </div>

        <div class="field">
          <label>العملة</label>

          <InputText v-model="localForm.currency" maxlength="3" class="w-full" />
        </div>

        <div class="field">
          <label>التاريخ</label>

          <DatePicker v-model="localForm.occurred_on" dateFormat="yy-mm-dd" class="w-full" />
        </div>

        <div class="field">
          <label>الفئة</label>

          <Select
            v-model="localForm.category"
            :options="categories"
            optionLabel="name"
            optionValue="id"
            showClear
            class="w-full"
          />
        </div>

        <div class="field full">
          <label>ملاحظات إضافية</label>

          <Textarea v-model="localForm.notes" rows="3" class="w-full" />
        </div>
      </template>

      <!-- Budget -->
      <template v-else-if="formType === 'budget'">
        <div class="field full">
          <label>اسم الميزانية</label>

          <InputText v-model="localForm.name" class="w-full" />
        </div>

        <div class="field">
          <label>الفترة</label>

          <Select
            v-model="localForm.period"
            :options="['daily', 'weekly', 'monthly', 'yearly']"
            class="w-full"
          />
        </div>

        <div class="field">
          <label>الحد</label>

          <InputNumber v-model="localForm.limit_amount" :min="0" class="w-full" />
        </div>

        <div class="field">
          <label>العملة</label>

          <InputText v-model="localForm.currency" maxlength="3" class="w-full" />
        </div>

        <div class="field">
          <label>الفئة</label>

          <Select
            v-model="localForm.category"
            :options="categories"
            optionLabel="name"
            optionValue="id"
            showClear
            class="w-full"
          />
        </div>
      </template>

      <!-- Debt -->
      <template v-else-if="formType === 'debt'">
        <div class="field full">
          <label>اسم الدين</label>

          <InputText v-model="localForm.name" class="w-full" />
        </div>

        <div class="field">
          <label>الرصيد</label>

          <InputNumber v-model="localForm.balance" :min="0" class="w-full" />
        </div>

        <div class="field">
          <label>الحد الأدنى للسداد</label>

          <InputNumber v-model="localForm.minimum_payment" :min="0" class="w-full" />
        </div>

        <div class="field">
          <label>الفائدة %</label>

          <InputNumber v-model="localForm.interest_rate" :min="0" suffix="%" class="w-full" />
        </div>

        <div class="field">
          <label>العملة</label>

          <InputText v-model="localForm.currency" maxlength="3" class="w-full" />
        </div>

        <div class="field">
          <label>تاريخ الاستحقاق</label>

          <DatePicker v-model="localForm.due_date" dateFormat="yy-mm-dd" showIcon class="w-full" />
        </div>

        <div class="field">
          <label>الحالة</label>

          <Select
            v-model="localForm.status"
            :options="['active', 'paid', 'overdue', 'upcoming']"
            class="w-full"
          />
        </div>
      </template>

      <!-- Savings -->
      <template v-else-if="formType === 'savings'">
        <div class="field full">
          <label>اسم الهدف</label>

          <InputText v-model="localForm.name" class="w-full" />
        </div>

        <div class="field">
          <label>المبلغ المستهدف</label>

          <InputNumber v-model="localForm.target_amount" :min="0" class="w-full" />
        </div>

        <div class="field">
          <label>المبلغ الحالي</label>

          <InputNumber v-model="localForm.current_amount" :min="0" class="w-full" />
        </div>

        <div class="field">
          <label>العملة</label>

          <InputText v-model="localForm.currency" maxlength="3" class="w-full" />
        </div>

        <div class="field">
          <label>تاريخ الهدف</label>

          <DatePicker
            v-model="localForm.target_date"
            dateFormat="yy-mm-dd"
            showIcon
            class="w-full"
          />
        </div>
      </template>

      <!-- Loan -->
      <template v-else-if="formType === 'loan'">
        <div class="field">
          <label>الاتجاه</label>

          <Select
            v-model="localForm.direction"
            :options="[
              { label: 'أنا أقرضت', value: 'lent' },
              { label: 'أنا اقترضت', value: 'borrowed' },
            ]"
            optionLabel="label"
            optionValue="value"
            class="w-full"
          />
        </div>

        <div class="field">
          <label>الشخص</label>

          <InputText v-model="localForm.person" class="w-full" />
        </div>

        <div class="field">
          <label>الإجمالي</label>

          <InputNumber v-model="localForm.amount" :min="0" class="w-full" />
        </div>

        <div class="field">
          <label>المتبقي</label>

          <InputNumber v-model="localForm.remaining" :min="0" class="w-full" />
        </div>

        <div class="field">
          <label>العملة</label>

          <InputText v-model="localForm.currency" maxlength="3" class="w-full" />
        </div>

        <div class="field">
          <label>التاريخ</label>

          <DatePicker v-model="localForm.date" dateFormat="yy-mm-dd" showIcon class="w-full" />
        </div>

        <div class="field">
          <label>تاريخ الاستحقاق</label>

          <DatePicker v-model="localForm.due_date" dateFormat="yy-mm-dd" showIcon class="w-full" />
        </div>

        <div class="field">
          <label>الحالة</label>

          <Select
            v-model="localForm.status"
            :options="['upcoming', 'active', 'paid', 'overdue']"
            class="w-full"
          />
        </div>

        <div class="field full">
          <label>ملاحظات</label>

          <Textarea v-model="localForm.notes" rows="3" class="w-full" />
        </div>
      </template>

      <!-- Recurring -->
      <template v-else-if="formType === 'recurring'">
        <div class="field full">
          <label>الاسم</label>

          <InputText v-model="localForm.name" class="w-full" />
        </div>

        <div class="field">
          <label>النوع</label>

          <Select
            v-model="localForm.kind"
            :options="[
              { label: 'دخل', value: 'income' },
              { label: 'مصروف', value: 'expense' },
            ]"
            optionLabel="label"
            optionValue="value"
            class="w-full"
          />
        </div>

        <div class="field">
          <label>المبلغ</label>

          <InputNumber v-model="localForm.amount" :min="0" class="w-full" />
        </div>

        <div class="field">
          <label>التكرار</label>

          <Select
            v-model="localForm.frequency"
            :options="['daily', 'weekly', 'biweekly', 'semimonthly', 'monthly', 'yearly']"
            class="w-full"
          />
        </div>

        <div class="field">
          <label>المصدر</label>

          <InputText v-model="localForm.source" class="w-full" />
        </div>

        <div class="field">
          <label>التاريخ القادم</label>

          <DatePicker v-model="localForm.next_date" dateFormat="yy-mm-dd" showIcon class="w-full" />
        </div>

        <div class="field">
          <label>العملة</label>

          <InputText v-model="localForm.currency" maxlength="3" class="w-full" />
        </div>

        <div class="field full">
          <label>الوصف</label>

          <Textarea v-model="localForm.description" rows="3" class="w-full" />
        </div>
      </template>

      <!-- Habit -->
      <template v-else-if="formType === 'habit'">
        <div class="field full">
          <label>العادة</label>

          <InputText v-model="localForm.name" class="w-full" />
        </div>

        <div class="field">
          <label>الهدف</label>

          <InputNumber v-model="localForm.target" :min="0" class="w-full" />
        </div>

        <div class="field">
          <label>المدة بالأيام</label>

          <InputNumber v-model="localForm.duration_days" :min="1" class="w-full" />
        </div>

        <div class="field">
          <label>التقدم</label>

          <InputNumber v-model="localForm.progress" :min="0" class="w-full" />
        </div>

        <div class="field">
          <label>Streak</label>

          <InputNumber v-model="localForm.streak" :min="0" class="w-full" />
        </div>

        <div class="field">
          <label>البداية</label>

          <DatePicker
            v-model="localForm.started_on"
            dateFormat="yy-mm-dd"
            showIcon
            class="w-full"
          />
        </div>
      </template>
    </div>

    <template #footer>
      <Button label="إلغاء" text @click="$emit('cancel')" />

      <Button label="حفظ" icon="pi pi-check" :loading="saving" @click="$emit('save')" />
    </template>
  </Dialog>
</template>

<script setup>
import { computed, ref, watch } from 'vue'

import Dialog from 'primevue/dialog'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import Select from 'primevue/select'
import DatePicker from 'primevue/datepicker'
import Textarea from 'primevue/textarea'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false,
  },

  formType: {
    type: String,
    default: 'transaction',
  },

  editingId: {
    type: [Number, String, null],
    default: null,
  },

  form: {
    type: Object,
    default: () => ({}),
  },

  categories: {
    type: Array,
    default: () => [],
  },

  saving: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['update:visible', 'update:form', 'cancel', 'save'])

const localForm = ref({})

watch(
  () => props.form,
  (value) => {
    localForm.value = {
      ...value,
    }
  },
  {
    immediate: true,
    deep: true,
  },
)

watch(
  localForm,
  (value) => {
    emit('update:form', {
      ...value,
    })
  },
  {
    deep: true,
  },
)

const formTitle = computed(() => {
  const labels = {
    transaction: 'معاملة',
    budget: 'ميزانية',
    debt: 'دين',
    savings: 'هدف ادخار',
    loan: 'سلفة',
    recurring: 'تدفق متكرر',
    habit: 'عادة',
  }

  return `${props.editingId ? 'تعديل' : 'إضافة'} ${labels[props.formType] || ''}`
})
</script>
