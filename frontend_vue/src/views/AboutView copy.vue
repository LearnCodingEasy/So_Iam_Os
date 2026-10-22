<template>
  <div class="about-view-container bg-surface text-on-surface min-h-screen p-6">
    <!-- رأس الصفحة باستخدام مكون Menubar -->

    <!-- شريط الإشعارات والتحكم السريع -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
      <prime_message severity="info" :closable="false">
        مرحباً بك يا حسام. تم ربط النظام بنجاح مع Django REST Framework وقنوات WebSocket.
      </prime_message>
      <div
        class="flex items-center gap-3 bg-surface-card p-4 rounded-xl border border-surface-border shadow-sm"
      >
        <prime_progress_spinner style="width: 30px; height: 30px" strokeWidth="6" />
        <span class="text-sm font-medium">حالة الخادم: متصل ومستقر (100%)</span>
      </div>
      <div
        class="flex items-center justify-end gap-2 bg-surface-card p-4 rounded-xl border border-surface-border shadow-sm"
      >
        <span class="text-sm">وضع العرض:</span>
        <prime_select_button v-model="viewMode" :options="viewOptions" optionLabel="name" />
      </div>
    </div>

    <!-- المحتوى الرئيسي مقسم باستخدام Stepper ولوحات Fieldset و Card -->
    <main class="space-y-8">
      <!-- قسم النماذج والتحكم الكامل بمكونات PrimeVue -->
      <prime_card class="shadow-lg border border-surface-border">
        <template #title>
          <div class="flex items-center justify-between">
            <span class="text-xl font-bold">لوحة التحكم والنماذج التفاعلية</span>
            <prime_tag value="PrimeVue Core Suite" severity="contrast" />
          </div>
        </template>
        <template #content>
          <prime_fluid>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <!-- حقل النص العادي مع FloatLabel -->
              <prime_float_label>
                <prime_input_text id="username" v-model="form.username" />
                <label for="username">اسم المستخدم / المشروع</label>
              </prime_float_label>

              <!-- حقل الأرقام -->
              <prime_float_label>
                <prime_input_number id="tokens" v-model="form.tokens" :min="0" :max="32000" />
                <label for="tokens">حد الـ Tokens المخصص</label>
              </prime_float_label>

              <!-- قائمة الاختيار Select -->
              <prime_float_label>
                <prime_select
                  id="model"
                  v-model="form.selectedModel"
                  :options="modelsList"
                  optionLabel="label"
                  class="w-full"
                />
                <label for="model">اختر نموذج الذكاء الاصطناعي</label>
              </prime_float_label>

              <!-- حقل كلمة المرور -->
              <prime_float_label>
                <prime_input_password id="pwd" v-model="form.password" toggleMask />
                <label for="pwd">مفتاح المصادقة API Key</label>
              </prime_float_label>

              <!-- منتقي التاريخ DatePicker -->
              <prime_float_label>
                <prime_date_picker id="date" v-model="form.date" showIcon />
                <label for="date">تاريخ الجلسة</label>
              </prime_float_label>

              <!-- منتقي الألوان ColorPicker -->
              <div
                class="flex items-center justify-between p-3 border border-surface-border rounded-lg"
              >
                <span class="text-sm font-medium">لون السمة النشطة:</span>
                <prime_color_picker v-model="form.themeColor" />
              </div>
            </div>

            <!-- مجموعة عناصر المدخلات InputGroup و ToggleSwitch -->
            <div class="mt-6 grid grid-cols-1 md:grid-cols-2 gap-6 items-center">
              <prime_input_group>
                <prime_input_group_addon>
                  <i class="pi pi-search"></i>
                </prime_input_group_addon>
                <prime_input_text placeholder="بحث شامل في المستندات و Knowledge Vault..." />
                <prime_button label="بحث" icon="pi pi-search" />
              </prime_input_group>

              <div
                class="flex items-center justify-around p-4 bg-surface-card rounded-lg border border-surface-border"
              >
                <div class="flex items-center gap-2">
                  <prime_toggle_switch v-model="form.notificationsActive" />
                  <span class="text-sm">تنبيهات الفورية</span>
                </div>
                <div class="flex items-center gap-2">
                  <prime_toggle_button
                    v-model="form.syncStatus"
                    onLabel="مزامنة مفعلة"
                    offLabel="مزامنة متوقفة"
                  />
                </div>
              </div>
            </div>

            <!-- أزرار الإجراءات والشارات والمؤشرات -->
            <div class="mt-6 flex flex-wrap items-center gap-4 pt-4 border-t border-surface-border">
              <prime_button
                label="حفظ التغييرات"
                icon="pi pi-check"
                severity="success"
                @click="showToast('success', 'تم الحفظ', 'تم تحديث الإعدادات بنجاح')"
              />
              <prime_button label="إعادة ضبط" icon="pi pi-refresh" severity="secondary" outlined />
              <prime_button
                label="حذف الجلسة"
                icon="pi pi-trash"
                severity="danger"
                @click="confirmDelete"
              />

              <div class="ms-auto flex items-center gap-3">
                <prime_overlay_badge value="4" severity="danger">
                  <prime_button icon="pi pi-bell" severity="contrast" text rounded />
                </prime_overlay_badge>
                <prime_chip label="Django 5.1" icon="pi pi-server" />
                <prime_chip label="Vue 3.4" icon="pi pi-code" class="bg-primary text-on-primary" />
              </div>
            </div>
          </prime_fluid>
        </template>
      </prime_card>

      <!-- قسم إدارة البيانات باستخدام DataTable و Paginator -->
      <prime_fieldset legend="سجل الأنشطة والعمليات (Jobs Pipeline)" :toggleable="true">
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <span class="text-sm text-surface-500"
              >عرض أحدث المهام والعمليات المزامنة عبر Celery وبطاقات الاستعلام</span
            >
            <prime_tag value="18 عملية قيد التشغيل" severity="info" />
          </div>

          <prime_data_table
            :value="jobsData"
            :paginator="true"
            :rows="5"
            class="p-datatable-sm border border-surface-border rounded-lg overflow-hidden"
          >
            <prime_column field="id" header="معرف المهمة" sortable></prime_column>
            <prime_column field="name" header="اسم العملية" sortable></prime_column>
            <prime_column field="status" header="الحالة">
              <template #body="slotProps">
                <prime_tag
                  :value="slotProps.data.status"
                  :severity="slotProps.data.status === 'مكتمل' ? 'success' : 'warn'"
                />
              </template>
            </prime_column>
            <prime_column field="duration" header="الوقت المستغرق" sortable></prime_column>
          </prime_data_table>
        </div>
      </prime_fieldset>

      <!-- قسم Stepper و الخطوات التعليمية / المعمارية -->
      <prime_card>
        <template #title>مخطط العمليات والخطوات المعمارية</template>
        <template #content>
          <prime_stepper value="1">
            <prime_step_list>
              <prime_step value="1">التوثيق والمدخلات</prime_step>
              <prime_step value="2">التحليل بالذكاء الاصطناعي</prime_step>
              <prime_step value="3">النشر والتنفيذ</prime_step>
            </prime_step_list>
            <prime_step_panels>
              <prime_step_panel value="1">
                <p class="mb-4 text-surface-600">
                  تحميل وتحليل ملفات DDL وملفات السيرفر الخاصة بقاعدة بيانات PostgreSQL.
                </p>
                <prime_file_upload
                  mode="basic"
                  name="demo[]"
                  url="./upload"
                  chooseLabel="اختر ملف المعمارية"
                />
              </prime_step_panel>
              <prime_step_panel value="2">
                <p class="mb-4 text-surface-600">
                  توليد شفرة الـ Composable والـ Pinia Stores باستخدام نماذج Claude و GPT.
                </p>
                <prime_slider v-model="sliderValue" class="w-full mb-4" />
                <span>مستوى العشوائية والحرية (Temperature): {{ sliderValue }}%</span>
              </prime_step_panel>
              <prime_step_panel value="3">
                <p class="mb-4 text-surface-600">
                  بث الأحداث الفورية عبر قنوات WebSocket وبدون إجهاد الـ API.
                </p>
                <prime_progress_bar :value="85" class="w-full" />
              </prime_step_panel>
            </prime_step_panels>
          </prime_stepper>
        </template>
      </prime_card>

      <!-- محرر النصوص الغنية Editor والملاحظات -->
      <prime_card>
        <template #title>محرر الملاحظات المتقدم (Quill Editor)</template>
        <template #content>
          <prime_editor v-model="editorContent" editorStyle="height: 180px" />
          <div class="mt-4 flex gap-3">
            <prime_button
              label="معاينة الشفرة"
              icon="pi pi-eye"
              outlined
              @click="visibleDialog = true"
            />
            <prime_button
              label="تحميل الملفات كـ ZIP"
              icon="pi pi-download"
              severity="help"
              @click="triggerDownload"
            />
          </div>
        </template>
      </prime_card>
    </main>

    <!-- نافذة منبثقة Dialog لعرض المعاينة -->
    <prime_dialog
      v-model:visible="visibleDialog"
      header="معاينة شفرة المكونات والتكامل"
      :style="{ width: '50vw' }"
      modal
    >
      <div class="p-4 bg-surface-900 text-surface-0 rounded-lg font-mono text-sm">
        <pre><code>// محاكاة مخرجات المكونات المعمارية لـ So_Iam_OS
import { useJobsPipelineStore } from '@/stores/jobsPipeline';
export function useJobTelemetry() {
  const store = useJobsPipelineStore();
  return { store, status: 'Connected via DRF Channels' };
}</code></pre>
      </div>
      <template #footer>
        <prime_button label="إغلاق" icon="pi pi-times" @click="visibleDialog = false" text />
      </template>
    </prime_dialog>

    <!-- عناصر النظام الإضافية للتأكيد والتنبيهات -->
    <prime_toast />
    <prime_confirm_dialog />
  </div>
</template>

<script>
import { ref } from 'vue'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'

export default {
  name: 'AboutView',
  setup() {
    const toast = useToast()
    const confirm = useConfirm()

    const viewMode = ref({ name: 'نشط', code: 'ACTIVE' })
    const viewOptions = ref([
      { name: 'نشط', code: 'ACTIVE' },
      { name: 'مرحباً', code: 'WELCOME' },
      { name: 'خطأ', code: 'ERROR' },
    ])

    const form = ref({
      username: 'Hossam Rashad Aboud',
      tokens: 4820,
      selectedModel: { label: 'Claude 3.5 Sonnet', value: 'claude' },
      password: '',
      date: new Date(),
      themeColor: '10b981',
      notificationsActive: true,
      syncStatus: true,
    })

    const modelsList = ref([
      { label: 'Claude 3.5 Sonnet', value: 'claude' },
      { label: 'GPT-4o', value: 'gpt4' },
      { label: 'Local Codex', value: 'ollama' },
    ])

    const jobsData = ref([
      { id: '#JOB-8842', name: 'Celery Beat Sync Telemetry', status: 'مكتمل', duration: '14ms' },
      {
        id: '#JOB-8843',
        name: 'PostgreSQL Partition 10M Rows',
        status: 'قيد التنفيذ',
        duration: '120ms',
      },
      { id: '#JOB-8844', name: 'WebSocket Broadcast Channels', status: 'مكتمل', duration: '22ms' },
      { id: '#JOB-8845', name: 'Vue 3 Pinia State Hydration', status: 'مكتمل', duration: '5ms' },
    ])

    const sliderValue = ref(70)
    const editorContent = ref('<p>اكتب ملاحظاتك الهندسية هنا...</p>')
    const visibleDialog = ref(false)

    const showToast = (severity, summary, detail) => {
      toast.add({ severity, summary, detail, life: 3000 })
    }

    const confirmDelete = () => {
      confirm.require({
        message: 'هل أنت متأكد من رغبتك في حذف هذه الجلسة والبيانات المؤقتة؟',
        header: 'تأكيد الحذف',
        icon: 'pi pi-exclamation-triangle',
        accept: () => {
          showToast('error', 'تم الحذف', 'تم مسح الجلسة بنجاح')
        },
      })
    }

    const triggerDownload = () => {
      showToast('info', 'جاري التجهيز', 'تم بدء تصدير الملفات كأرشيف ZIP')
    }

    const menuItems = ref([
      { label: 'الرئيسية', icon: 'pi pi-home' },
      { label: 'الورشة البرمجية', icon: 'pi pi-code' },
      { label: 'المستندات', icon: 'pi pi-book' },
      { label: 'الإعدادات', icon: 'pi pi-cog' },
    ])

    return {
      viewMode,
      viewOptions,
      form,
      modelsList,
      jobsData,
      sliderValue,
      editorContent,
      visibleDialog,
      menuItems,
      showToast,
      confirmDelete,
      triggerDownload,
    }
  },
}
</script>

<style lang="scss" scoped>
.about-view-container {
  font-family: inherit;
}
</style>
