<template>
  <div class="finance-page" dir="rtl">
    <div class="finance-shell">
      <FinanceHero
        :loading="loading"
        :api-checking="apiChecking"
        @refresh="loadAll"
        @check-apis="checkApis"
        @add-transaction="openForm('transaction')"
      />

      <Message
        v-if="pageError"
        severity="error"
        :closable="true"
        class="page-message"
        @close="pageError = ''"
      >
        {{ pageError }}
      </Message>

      <FinanceKpiGrid :metrics="metrics" />

      <FinanceHealthAlerts
        :health="health"
        :health-severity="healthSeverity"
        :alerts="alerts"
        :health-label="healthLabel"
        :alert-severity="alertSeverity"
        @mark-alert="markAlert"
      />

      <FinanceSectionNav v-model="section" :sections="sections" />

      <!-- Overview -->
      <FinanceOverview
        v-if="section === 'overview'"
        :flow="flow"
        :period-label="periodLabel"
        :insights="insights"
        :transactions="transactions"
        :savings="savings"
        :base-currency="baseCurrency"
        :loading="loading"
        :ai-loading="aiLoading"
        :money="money"
        :goal-percent="goalPercent"
        :insight-type="insightType"
        :kind-label="kindLabel"
        :kind-severity="kindSeverity"
        @ask-ai="askAI"
        @go-transactions="section = 'transactions'"
      />

      <!-- Transactions -->
      <FinanceTransactions
        v-if="section === 'transactions'"
        :transactions="transactions"
        :loading="loading"
        :money="money"
        :kind-label="kindLabel"
        :kind-severity="kindSeverity"
        @add="openForm('transaction')"
        @edit="editItem('transaction', $event)"
        @remove="remove('transaction', $event)"
      />

      <!-- Budgets -->
      <FinanceBudgets
        v-if="section === 'budgets'"
        :budgets="budgets"
        :money="money"
        @add="openForm('budget')"
        @edit="editItem('budget', $event)"
        @remove="remove('budget', $event)"
      />

      <!-- Debts -->
      <FinanceDebts
        v-if="section === 'debts'"
        :debts="debts"
        :total-debt="totalDebt"
        :base-currency="baseCurrency"
        :money="money"
        @add="openForm('debt')"
        @payment="openDebtPayment"
        @edit="editItem('debt', $event)"
        @remove="remove('debt', $event)"
      />

      <!-- Savings -->
      <FinanceSavings
        v-if="section === 'savings'"
        :savings="savings"
        :saving-plan="savingPlan"
        :base-currency="baseCurrency"
        :money="money"
        :goal-percent="goalPercent"
        @add="openForm('savings')"
        @plan="makeSavingPlan"
        @edit="editItem('savings', $event)"
        @remove="remove('savings', $event)"
      />

      <!-- Forecast -->
      <FinanceForecast
        v-if="section === 'forecast'"
        :forecast-rows="forecastRows"
        :scenario-form="scenarioForm"
        :scenario-result="scenarioResult"
        :base-currency="baseCurrency"
        :money="money"
        @refresh="loadForecast"
        @scenario="runScenario"
      />

      <!-- Loans -->
      <FinanceLoans
        v-if="section === 'loans'"
        :loans="loans"
        :loan-totals="loanTotals"
        :base-currency="baseCurrency"
        :money="money"
        @add="openForm('loan')"
        @payment="openLoanPayment"
        @edit="editItem('loan', $event)"
        @remove="remove('loan', $event)"
      />

      <!-- Recurring -->
      <FinanceRecurring
        v-if="section === 'recurring'"
        :recurring="recurring"
        :subscriptions="subscriptions"
        :money="money"
        :kind-label="kindLabel"
        :kind-severity="kindSeverity"
        @add="openForm('recurring')"
        @edit="editItem('recurring', $event)"
        @remove="remove('recurring', $event)"
      />

      <!-- Habits -->
      <FinanceHabits
        v-if="section === 'habits'"
        :habits="habits"
        @add="openForm('habit')"
        @edit="editItem('habit', $event)"
        @remove="remove('habit', $event)"
      />

      <!-- Reports -->
      <FinanceReports
        v-if="section === 'reports'"
        :weekly-report="weeklyReport"
        :monthly-report="monthlyReport"
        :pretty="pretty"
      />

      <!-- AI Coach -->
      <FinanceCoach
        v-if="section === 'coach'"
        v-model:question="coachQuestion"
        :answer="coachAnswer"
        :loading="coachLoading"
        @ask="askCoach"
      />

      <!-- Integrations -->
      <FinanceIntegrations v-if="section === 'integrations'" :ecosystem="ecosystem" />

      <!-- API -->
      <FinanceApiTest
        v-if="section === 'api'"
        :api-results="apiResults"
        :api-checking="apiChecking"
        :api-passed="apiPassed"
        :api-failed="apiFailed"
      />
    </div>

    <!-- CRUD -->
    <FinanceCrudDialog
      v-model:visible="formVisible"
      :form-type="formType"
      :editing-id="editingId"
      :form="form"
      :categories="categories"
      :saving="saving"
      @update:form="form = $event"
      @cancel="formVisible = false"
      @save="saveForm"
    />

    <!-- Payment -->
    <FinancePaymentDialog
      v-model:visible="paymentVisible"
      :payment-form="paymentForm"
      :saving="saving"
      @update:payment-form="paymentForm = $event"
      @cancel="paymentVisible = false"
      @save="savePayment"
    />

    <ConfirmDialog />

    <Toast />
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'

import { useConfirm } from 'primevue/useconfirm'

import { useToast } from 'primevue/usetoast'

import api from '@/services/api'
import { financeApi } from '@/services/osDomains'

import FinanceHero from '@/components/Finance/FinanceHero.vue'
import FinanceKpiGrid from '@/components/Finance/FinanceKpiGrid.vue'
import FinanceHealthAlerts from '@/components/Finance/FinanceHealthAlerts.vue'
import FinanceSectionNav from '@/components/Finance/FinanceSectionNav.vue'

import FinanceOverview from '@/components/Finance/FinanceOverview.vue'
import FinanceTransactions from '@/components/Finance/FinanceTransactions.vue'
import FinanceBudgets from '@/components/Finance/FinanceBudgets.vue'
import FinanceDebts from '@/components/Finance/FinanceDebts.vue'
import FinanceSavings from '@/components/Finance/FinanceSavings.vue'
import FinanceForecast from '@/components/Finance/FinanceForecast.vue'
import FinanceLoans from '@/components/Finance/FinanceLoans.vue'
import FinanceRecurring from '@/components/Finance/FinanceRecurring.vue'
import FinanceHabits from '@/components/Finance/FinanceHabits.vue'
import FinanceReports from '@/components/Finance/FinanceReports.vue'
import FinanceCoach from '@/components/Finance/FinanceCoach.vue'
import FinanceIntegrations from '@/components/Finance/FinanceIntegrations.vue'
import FinanceApiTest from '@/components/Finance/FinanceApiTest.vue'

import FinanceCrudDialog from '@/components/Finance/FinanceCrudDialog.vue'
import FinancePaymentDialog from '@/components/Finance/FinancePaymentDialog.vue'

const toast = useToast()
const confirm = useConfirm()

const loading = ref(false)
const saving = ref(false)
const aiLoading = ref(false)
const coachLoading = ref(false)
const apiChecking = ref(false)

const pageError = ref('')

const section = ref('overview')

const sections = [
  { label: 'نظرة عامة', value: 'overview' },
  { label: 'المعاملات', value: 'transactions' },
  { label: 'الميزانيات', value: 'budgets' },
  { label: 'الديون', value: 'debts' },
  { label: 'الادخار', value: 'savings' },
  { label: 'Forecast', value: 'forecast' },
  { label: 'السلف', value: 'loans' },
  { label: 'المتكرر', value: 'recurring' },
  { label: 'العادات', value: 'habits' },
  { label: 'التقارير', value: 'reports' },
  { label: 'AI Coach', value: 'coach' },
  { label: 'التكامل', value: 'integrations' },
  { label: 'API Test', value: 'api' },
]

const summary = ref({})
const dashboard = ref({})
const insights = ref({
  insights: [],
  disclaimer: '',
})

const health = ref({
  score: 0,
  components: {},
})

const transactions = ref([])
const categories = ref([])
const budgets = ref([])
const debts = ref([])
const savings = ref([])
const subscriptions = ref([])
const loans = ref([])
const recurring = ref([])
const habits = ref([])
const alerts = ref([])

const forecastData = ref({
  forecast: [],
})

const weeklyReport = ref({})
const monthlyReport = ref({})

const savingPlan = ref(null)
const scenarioResult = ref(null)

const coachQuestion = ref('')
const coachAnswer = ref('')

const apiResults = ref([])

const ecosystem = ref({
  connections: {},
  recommended_flow: [],
  income_opportunities: 0,
})

const formVisible = ref(false)
const paymentVisible = ref(false)

const formType = ref('transaction')
const editingId = ref(null)
const form = ref({})

const paymentForm = ref({
  amount: 0,
  paid_on: new Date(),
  note: '',
})

const selectedDebt = ref(null)
const selectedLoan = ref(null)

const scenarioForm = ref({
  income_change_percent: 0,
  expense_change_percent: 0,
  extra_debt_payment: 0,
  case: 'expected',
})

const baseCurrency = computed(() => dashboard.value.base_currency || 'USD')

const totalDebt = computed(() =>
  debts.value.reduce((sum, debt) => sum + Number(debt.balance || 0), 0),
)

const loanTotals = computed(() => ({
  lent: loans.value
    .filter((item) => item.direction === 'lent')
    .reduce((sum, item) => sum + Number(item.remaining || 0), 0),

  borrowed: loans.value
    .filter((item) => item.direction === 'borrowed')
    .reduce((sum, item) => sum + Number(item.remaining || 0), 0),
}))

const metrics = computed(() => [
  {
    label: 'الرصيد الصافي',
    value: money(summary.value.balance, baseCurrency.value),
    icon: 'pi pi-wallet',
    help: 'بعد المصروفات والادخار والديون',
  },

  {
    label: 'الدخل',
    value: money(summary.value.income, baseCurrency.value),
    icon: 'pi pi-arrow-down-left',
    help: 'الفترة الحالية',
  },

  {
    label: 'المصروفات',
    value: money(summary.value.expenses, baseCurrency.value),
    icon: 'pi pi-arrow-up-right',
    help: 'الفترة الحالية',
  },

  {
    label: 'الادخار',
    value: money(summary.value.savings, baseCurrency.value),
    icon: 'pi pi-piggy-bank',
    help: 'المسجل فعليًا',
  },

  {
    label: 'الديون',
    value: money(totalDebt.value, baseCurrency.value),
    icon: 'pi pi-credit-card',
    help: 'الرصيد النشط',
  },
])

const periodLabel = computed(() =>
  dashboard.value.period
    ? `${dashboard.value.period.from} — ${dashboard.value.period.to}`
    : 'الفترة الحالية',
)

const flow = computed(() => {
  const rows = [
    ['الدخل', summary.value.income || 0],
    ['المصروفات', summary.value.expenses || 0],
    ['الادخار', summary.value.savings || 0],
    ['سداد الديون', summary.value.debt_payments || 0],
  ]

  const max = Math.max(...rows.map((row) => Number(row[1])), 1)

  return rows.map(([label, value]) => ({
    label,
    value,
    percent: Math.max(4, Math.min(100, Math.round((Number(value) / max) * 100))),
  }))
})

const forecastRows = computed(() => forecastData.value.forecast || [])

const healthSeverity = computed(() => {
  const score = Number(health.value.score || 0)

  if (score >= 80) return 'success'
  if (score >= 60) return 'info'
  if (score >= 40) return 'warn'

  return 'danger'
})

const apiPassed = computed(() => apiResults.value.filter((item) => item.ok).length)

const apiFailed = computed(() => apiResults.value.some((item) => !item.ok))

function normalizeCurrency(value) {
  const currency = String(value || '')
    .trim()
    .toUpperCase()

  return /^[A-Z]{3}$/.test(currency) ? currency : 'USD'
}

function money(value, currency = 'USD') {
  const numeric = Number(value || 0)

  const normalized = normalizeCurrency(currency)

  try {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: normalized,
      maximumFractionDigits: 2,
    }).format(numeric)
  } catch {
    return `${numeric.toFixed(2)} ${normalized}`
  }
}

function healthLabel(key) {
  return (
    {
      spending_control: 'التحكم في الإنفاق',

      savings: 'الادخار',

      debt_management: 'إدارة الديون',

      goal_progress: 'تقدم الأهداف',

      budget_adherence: 'الميزانيات',

      income_stability: 'استقرار الدخل',
    }[key] || key
  )
}

function alertSeverity(value) {
  return (
    {
      danger: 'danger',
      warning: 'warn',
      info: 'info',
    }[value] || 'info'
  )
}

function insightType(value) {
  return (
    {
      warning: 'تحذير',
      saving: 'ادخار',
      goal: 'هدف',
      bill: 'فاتورة',
      info: 'معلومة',
    }[value] || 'معلومة'
  )
}

function kindLabel(value) {
  return (
    {
      income: 'دخل',
      expense: 'مصروف',
      saving: 'ادخار',
      debt_payment: 'سداد دين',
    }[value] || value
  )
}

function kindSeverity(value) {
  return (
    {
      income: 'success',
      expense: 'danger',
      saving: 'info',
      debt_payment: 'warn',
    }[value] || 'info'
  )
}

function goalPercent(goal) {
  const target = Number(goal.target_amount || 0)

  if (!target) return 0

  return Math.min(100, Math.round((Number(goal.current_amount || 0) / target) * 100))
}

function pretty(value) {
  return JSON.stringify(value || {}, null, 2)
}

function dateValue(value) {
  if (!value) return null

  const date = value instanceof Date ? value : new Date(`${String(value).slice(0, 10)}T00:00:00`)

  return Number.isNaN(date.getTime()) ? null : date
}

function apiDate(value) {
  const date = dateValue(value)
  return date ? date.toISOString().slice(0, 10) : null
}

function clean(payload) {
  const output = { ...payload }

  for (const key of [
    'occurred_on',
    'due_date',
    'target_date',
    'next_date',
    'started_on',
    'paid_on',
    'date',
  ]) {
    if (key in output) {
      output[key] = apiDate(output[key])
    }
  }

  if (output.currency) {
    output.currency = String(output.currency).toUpperCase()
  }

  return output
}

function formDefaults(type) {
  const today = new Date()

  const defaults = {
    transaction: {
      description: '',
      kind: 'expense',
      amount: 0,
      currency: baseCurrency.value,
      occurred_on: today,
      category: null,
      notes: '',
    },

    budget: {
      name: '',
      period: 'monthly',
      limit_amount: 0,
      currency: baseCurrency.value,
      category: null,
      active: true,
    },

    debt: {
      name: '',
      balance: 0,
      minimum_payment: 0,
      interest_rate: 0,
      currency: baseCurrency.value,
      due_date: null,
      status: 'active',
    },

    savings: {
      name: '',
      target_amount: 0,
      current_amount: 0,
      currency: baseCurrency.value,
      target_date: null,
      status: 'active',
    },

    loan: {
      direction: 'lent',
      person: '',
      amount: 0,
      remaining: 0,
      currency: baseCurrency.value,
      date: today,
      due_date: null,
      status: 'upcoming',
      notes: '',
    },

    recurring: {
      name: '',
      kind: 'expense',
      amount: 0,
      currency: baseCurrency.value,
      frequency: 'monthly',
      source: '',
      next_date: today,
      active: true,
      description: '',
    },

    habit: {
      name: '',
      target: 0,
      duration_days: 30,
      progress: 0,
      streak: 0,
      started_on: today,
      status: 'active',
      reminder_time: null,
    },
  }

  return { ...(defaults[type] || {}) }
}

function openForm(type) {
  formType.value = type
  editingId.value = null
  form.value = formDefaults(type)
  formVisible.value = true
}

function editItem(type, item) {
  formType.value = type
  editingId.value = item.id
  form.value = { ...item }

  for (const key of ['occurred_on', 'due_date', 'target_date', 'next_date', 'started_on', 'date']) {
    if (key in form.value) {
      form.value[key] = dateValue(form.value[key])
    }
  }

  formVisible.value = true
}

async function saveForm() {
  saving.value = true

  try {
    const payload = clean(form.value)
    const id = editingId.value

    const actions = {
      transaction: id
        ? () => financeApi.updateTransaction(id, payload)
        : () => financeApi.addTransaction(payload),

      budget: id
        ? () => financeApi.updateBudget(id, payload)
        : () => financeApi.createBudget(payload),

      debt: id ? () => financeApi.updateDebt(id, payload) : () => financeApi.createDebt(payload),

      savings: id
        ? () => financeApi.updateSavings(id, payload)
        : () => financeApi.createSavings(payload),

      loan: id
        ? () => financeApi.updateLoan(id, payload)
        : () =>
            financeApi.createLoan({
              ...payload,
              remaining: payload.remaining || payload.amount,
            }),

      recurring: id
        ? () => financeApi.updateRecurringCashflow(id, payload)
        : () => financeApi.createRecurringCashflow(payload),

      habit: id ? () => financeApi.updateHabit(id, payload) : () => financeApi.createHabit(payload),
    }

    if (!actions[formType.value]) {
      throw new Error('هذا النوع غير مدعوم من Finance API.')
    }

    await actions[formType.value]()

    formVisible.value = false

    toast.add({
      severity: 'success',
      summary: 'تم الحفظ',
      detail: 'تم تحديث البيانات المالية',
      life: 2500,
    })

    await loadAll()
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'فشل الحفظ',
      detail: apiErrorMessage(error),
      life: 4500,
    })
  } finally {
    saving.value = false
  }
}

function remove(type, item) {
  confirm.require({
    message: `هل تريد حذف ${item.name || item.person || item.description || 'العنصر'}؟`,
    header: 'تأكيد الحذف',
    icon: 'pi pi-exclamation-triangle',
    rejectLabel: 'إلغاء',
    acceptLabel: 'حذف',
    acceptClass: 'p-button-danger',

    accept: async () => {
      try {
        const actions = {
          transaction: () => financeApi.removeTransaction(item.id),

          budget: () => financeApi.removeBudget(item.id),

          debt: () => financeApi.removeDebt(item.id),

          savings: () => financeApi.removeSavings(item.id),

          loan: () => financeApi.removeLoan(item.id),

          recurring: () => financeApi.removeRecurringCashflow(item.id),

          habit: () => financeApi.removeHabit(item.id),
        }

        if (!actions[type]) {
          throw new Error('عملية الحذف غير مدعومة.')
        }

        await actions[type]()

        toast.add({
          severity: 'success',
          summary: 'تم الحذف',
          detail: 'تم حذف العنصر بنجاح',
          life: 2200,
        })

        await loadAll()
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'فشل الحذف',
          detail: apiErrorMessage(error),
          life: 4000,
        })
      }
    },
  })
}

function openDebtPayment(debt) {
  selectedDebt.value = debt
  selectedLoan.value = null

  paymentForm.value = {
    amount: 0,
    paid_on: new Date(),
    note: '',
  }

  paymentVisible.value = true
}

function openLoanPayment(loan) {
  selectedLoan.value = loan
  selectedDebt.value = null

  paymentForm.value = {
    amount: 0,
    paid_on: new Date(),
    note: '',
  }

  paymentVisible.value = true
}

async function savePayment() {
  saving.value = true

  try {
    const payload = clean(paymentForm.value)

    if (selectedDebt.value) {
      await financeApi.payDebt(selectedDebt.value.id, payload)
    } else if (selectedLoan.value) {
      await financeApi.payLoan(selectedLoan.value.id, payload)
    } else {
      throw new Error('لم يتم اختيار دين أو سلفة.')
    }

    paymentVisible.value = false

    toast.add({
      severity: 'success',
      summary: 'تم تسجيل الدفعة',
      detail: 'تم تحديث الرصيد',
      life: 2200,
    })

    await loadAll()
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'فشل السداد',
      detail: apiErrorMessage(error),
      life: 4000,
    })
  } finally {
    saving.value = false
  }
}

async function makeSavingPlan(goal) {
  try {
    savingPlan.value = await financeApi.createSavingPlan(goal.id)

    toast.add({
      severity: 'success',
      summary: 'تم إنشاء الخطة',
      life: 2200,
    })
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'تعذر إنشاء الخطة',
      detail: apiErrorMessage(error),
      life: 3500,
    })
  }
}

async function markAlert(alert) {
  try {
    await financeApi.markAlertRead(alert.id)

    alerts.value = alerts.value.filter((item) => item.id !== alert.id)
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'تعذر تحديث التنبيه',
      detail: apiErrorMessage(error),
      life: 3000,
    })
  }
}

async function loadForecast() {
  try {
    forecastData.value = await financeApi.forecast(6)
  } catch (error) {
    pageError.value = 'تعذر تحميل التوقع المالي من الخادم.'
  }
}

async function runScenario() {
  try {
    scenarioResult.value = await financeApi.scenario(scenarioForm.value)
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'تعذر حساب السيناريو',
      detail: apiErrorMessage(error),
      life: 3500,
    })
  }
}

async function askAI() {
  aiLoading.value = true

  try {
    const result = await financeApi.aiInsights({
      share_with_ai: true,
    })

    insights.value = result.content
      ? {
          disclaimer: result.disclaimer,
          insights: [
            {
              type: 'info',
              title: 'تحليل AI',
              detail: result.content,
            },
          ],
        }
      : result.fallback || {
          insights: [],
          disclaimer: '',
        }

    toast.add({
      severity: 'success',
      summary: 'تم التحليل',
      life: 2200,
    })
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'تعذر التحليل',
      detail: apiErrorMessage(error),
      life: 4000,
    })
  } finally {
    aiLoading.value = false
  }
}

async function askCoach() {
  if (!coachQuestion.value.trim()) return

  coachLoading.value = true

  try {
    const result = await financeApi.coach(coachQuestion.value.trim())

    coachAnswer.value = result.answer || result.content || 'لم يصل رد من AI.'
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'تعذر الرد',
      detail: apiErrorMessage(error),
      life: 4000,
    })
  } finally {
    coachLoading.value = false
  }
}

async function checkApis() {
  apiChecking.value = true
  apiResults.value = []

  try {
    const contract = await financeApi.contract()

    const paths = (contract.endpoints || []).filter(
      (path) => !path.includes('{id}') && !path.endsWith('ai_insights/'),
    )

    const results = await Promise.all(
      paths.map(async (path) => {
        const started = performance.now()

        try {
          const requestPath = path.startsWith('/api/') ? path.replace('/api', '') : path

          const response = await api.get(requestPath)

          return {
            method: 'GET',
            path,
            status: response.status,
            ok: true,
            duration: Math.round(performance.now() - started),
            error: '',
          }
        } catch (error) {
          return {
            method: 'GET',
            path,
            status: error?.response?.status || 0,
            ok: false,
            duration: Math.round(performance.now() - started),
            error: apiErrorMessage(error),
          }
        }
      }),
    )

    apiResults.value = results

    toast.add({
      severity: results.every((item) => item.ok) ? 'success' : 'warn',
      summary: 'اكتمل فحص APIs',
      detail: `PASS ${results.filter((item) => item.ok).length} / ${results.length}`,
      life: 3500,
    })
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'فشل فحص العقد',
      detail: apiErrorMessage(error),
      life: 4000,
    })
  } finally {
    apiChecking.value = false
  }
}

async function loadAll() {
  loading.value = true
  pageError.value = ''

  const results = await Promise.allSettled([
    financeApi.summary(),
    financeApi.dashboard(),
    financeApi.insights(),
    financeApi.health(),
    financeApi.transactions(),
    financeApi.categories(),
    financeApi.budgets(),
    financeApi.debts(),
    financeApi.savings(),
    financeApi.subscriptions(),
    financeApi.loans(),
    financeApi.recurringCashflows(),
    financeApi.habits(),
    financeApi.alerts(),
    financeApi.weeklyReport(),
    financeApi.monthlyReport(),
    financeApi.forecast(6),
    financeApi.ecosystem(),
  ])

  const [
    summaryResult,
    dashboardResult,
    insightsResult,
    healthResult,
    transactionsResult,
    categoriesResult,
    budgetsResult,
    debtsResult,
    savingsResult,
    subscriptionsResult,
    loansResult,
    recurringResult,
    habitsResult,
    alertsResult,
    weeklyResult,
    monthlyResult,
    forecastResult,
    ecosystemResult,
  ] = results

  const value = (result, fallback) => (result.status === 'fulfilled' ? result.value : fallback)

  summary.value = value(summaryResult, {})

  dashboard.value = value(dashboardResult, {})

  insights.value = value(insightsResult, {
    insights: [],
    disclaimer: '',
  })

  health.value = value(healthResult, {
    score: 0,
    components: {},
  })

  transactions.value = value(transactionsResult, [])

  categories.value = value(categoriesResult, [])

  budgets.value = value(budgetsResult, [])

  debts.value = value(debtsResult, [])

  savings.value = value(savingsResult, [])

  subscriptions.value = value(subscriptionsResult, [])

  loans.value = value(loansResult, [])

  recurring.value = value(recurringResult, [])

  habits.value = value(habitsResult, [])

  alerts.value = value(alertsResult, [])

  weeklyReport.value = value(weeklyResult, {})

  monthlyReport.value = value(monthlyResult, {})

  forecastData.value = value(forecastResult, {
    forecast: [],
  })

  ecosystem.value = value(ecosystemResult, {
    connections: {},
    recommended_flow: [],
    income_opportunities: 0,
  })

  const failed = results.filter((result) => result.status === 'rejected').length

  if (failed) {
    pageError.value =
      `تم تحميل البيانات المتاحة، لكن ${failed} من خدمات Finance لم تستجب. ` +
      'استخدم API Test لمعرفة الـ endpoint المتسبب في المشكلة.'
  }

  loading.value = false
}

function apiErrorMessage(error) {
  const data = error?.response?.data

  if (typeof data === 'string' && data.trim()) {
    return data
  }

  if (data?.detail) return String(data.detail)
  if (data?.message) return String(data.message)
  if (data?.error) return String(data.error)

  if (data && typeof data === 'object') {
    const first = Object.values(data)[0]

    if (Array.isArray(first)) {
      return String(first[0])
    }

    if (first) return String(first)
  }

  return error?.message || 'حدث خطأ غير متوقع.'
}

/*
 * مهم:
 * هنا تحتفظ بنفس functions الموجودة
 * في ملفك الأصلي:
 *
 *
 * apiDate
 * clean
 * formDefaults
 * openForm
 * editItem
 * saveForm
 * remove
 * openDebtPayment
 * openLoanPayment
 * savePayment
 * makeSavingPlan
 * markAlert
 * loadForecast
 * runScenario
 * askAI
 * askCoach
 * checkApis
 * loadAll
 * apiErrorMessage
 */

onMounted(loadAll)
</script>
