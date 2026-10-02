// ============================================================
//  usePrograms.js
//  src/composables/usePrograms.js
//
//  الـ Composable ده بيجمع كل اللوجيك الخاص بالـ Programs
//  من ناحية الـ View (dialogs، validation، async actions)
//
//  الـ split بين الـ store والـ composable:
//  ┌──────────────────┬──────────────────────────────┐
//  │  useProgramStore │  usePrograms composable       │
//  ├──────────────────┼──────────────────────────────┤
//  │  programs[]      │  createProgramVisible         │
//  │  form{}          │  editProgramVisible           │
//  │  CRUD API calls  │  useAsyncAction + toasts      │
//  │  validation      │  confirm dialogs              │
//  └──────────────────┴──────────────────────────────┘
// ============================================================

import { ref }              from 'vue'
import { useConfirm }       from 'primevue/useconfirm'
import { useToastHelper }   from '@/composables/useToastHelper'
import { useAsyncAction }   from '@/composables/useAsyncAction'
import { useProgramStore }  from '@/stores/useProgramStore'

export function usePrograms() {
  const confirm       = useConfirm()
  const { warn, cancelled, apiError } = useToastHelper()
  const programAction = useAsyncAction()
  const programStore  = useProgramStore()

  // Dialog State — مش في الـ store
  const createProgramVisible = ref(false)
  const editProgramVisible   = ref(false)

  // ─────────── Image Upload ───────────
  const onImageChange = (e) => {
    const err = programStore.onImageChange(e)
    if (err) warn('الملف كبير', err)
  }

  // ─────────── CREATE ───────────
  const createProgram = () =>
    programAction.run(
      () => programStore.createProgram(),
      {
        validate:       () => programStore.validateForm(),
        successSummary: 'تم إنشاء البرنامج',
        successDetail:  `"${programStore.form.name}" أُنشئ بنجاح`,
        errorSummary:   'فشل إنشاء البرنامج',
        onSuccess: () => { createProgramVisible.value = false },
      },
    )

  // ─────────── EDIT (open dialog) ───────────
  const openEditProgram = async (id) => {
    try {
      await programStore.loadProgram(id)
      editProgramVisible.value = true
    } catch (err) {
      apiError(err, 'فشل تحميل البيانات')
    }
  }

  // ─────────── UPDATE ───────────
  const editProgram = () =>
    programAction.run(
      () => programStore.updateProgram(programStore.currentProgramId),
      {
        validate:       () => programStore.validateForm(),
        successSummary: 'تم تحديث البرنامج',
        errorSummary:   'فشل تحديث البرنامج',
        onSuccess: () => { editProgramVisible.value = false },
      },
    )

  // ─────────── DELETE ───────────
  const confirmDeleteProgram = (program) => {
    confirm.require({
      message:     `هل أنت متأكد من حذف "${program.name}"؟`,
      header:      '⚠️ تأكيد الحذف',
      icon:        'pi pi-exclamation-triangle',
      acceptLabel: 'نعم، احذف',
      rejectLabel: 'إلغاء',
      accept: () =>
        programAction.run(
          () => programStore.deleteProgram(program.id),
          { successSummary: 'تم الحذف', successDetail: 'تم حذف البرنامج بنجاح', errorSummary: 'فشل الحذف' },
        ),
      reject: () => cancelled('لم يتم حذف البرنامج'),
    })
  }

  // ─────────── Controls ───────────
  const openProgram     = (id) => programAction.run(() => programStore.openProgram(id),     { errorSummary: 'فشل فتح البرنامج' })
  const closeProgram    = (id) => programAction.run(() => programStore.closeProgram(id),    { errorSummary: 'فشل إغلاق البرنامج' })
  const focusProgram    = (id) => programAction.run(() => programStore.focusProgram(id),    { successSummary: 'تم التركيز',  errorSummary: 'فشل التركيز' })
  const maximizeProgram = (id) => programAction.run(() => programStore.maximizeProgram(id), { successSummary: 'تم التكبير',  errorSummary: 'فشل التكبير' })
  const statusProgram   = (id) => programStore.statusProgram(id)  // مباشر — بدون loader

  // ─────────── Return ───────────
  return {
    programStore,
    createProgramVisible,
    editProgramVisible,
    loading: programAction.loading,
    onImageChange,
    createProgram,
    openEditProgram,
    editProgram,
    confirmDeleteProgram,
    openProgram,
    closeProgram,
    focusProgram,
    maximizeProgram,
    statusProgram,
  }
}
