<template>
  <div class="programs-page p-4">
    <h2 class="text-xl font-bold mb-4">Programs 🖥️</h2>

    <!-- زر إضافة برنامج -->
    <Button label="Create Program" icon="pi pi-plus" class="mb-4" @click="ceateProgramVisible = true" />

    <!-- جدول البرامج -->

    <div>
      <div class="flex justify-between items-center mb-3">
        <h3 class="text-lg font-bold">
          <prime_tag value="Programs" />
        </h3>
        <prime_button icon="pi pi-plus" @click="ceateProgramVisible = true"
          style="background-color: transparent; padding: 0; border: none">
          <prime_tag icon="pi pi-plus" />
        </prime_button>
      </div>
      <div class="wrapper_programs">
        <div class="" v-if="loadingPrograms">
          <prime_skeleton height="3rem" width="100%" class="mt-2" shape="circle" borderRadius="16px">
          </prime_skeleton>
          <prime_skeleton height="3rem" width="100%" class="mt-2" shape="circle" borderRadius="16px">
          </prime_skeleton>
          <prime_skeleton height="3rem" width="100%" class="mt-2" shape="circle" borderRadius="16px">
          </prime_skeleton>
        </div>
        <div v-for="p in programs" :key="p.id" class="p-1 rounded cursor-grab link_aside" draggable="true"
          @dragstart="startDrag({ type: 'program', id: p.id })" v-else @click="selectProgram(p.id)">
          <prime_image alt="Image" preview>
            <template #previewicon> <i class="pi pi-search"></i> </template>
            <template #image>
              <img :src="p.get_image" alt="image" />
            </template>
            <template #preview="slotProps">
              <img :src="p.get_image" alt="preview" :style="slotProps.style" @click="slotProps.onClick" />
            </template>
          </prime_image>
          <prime_tag :value="p.name" />
          <div class="">
            <prime_button icon="pi pi-plus" @click.stop="openEditProgram(p.id)"
              style="background-color: transparent; padding: 0; border: none">
              <prime_tag icon="pi pi-file-edit" />
            </prime_button>
            <prime_button icon="pi pi-plus" @click.stop="confirmDeleteProgram(p)"
              style="background-color: transparent; padding: 0; border: none">
              <prime_tag icon="pi pi-trash" />
            </prime_button>
          </div>
        </div>
      </div>
    </div>
    <!-- Ceate Program -->
    <div class="card flex justify-center">
      <!-- eslint-disable vue/no-v-model-argument -->

      <prime_dialog v-model:visible="ceateProgramVisible" pt:root:class="!border-0 !bg-transparent"
        pt:mask:class="backdrop-blur-sm">
        <template #container="{ closeCallback }">
          <div class="flex flex-col px-8 py-8 gap-6 rounded-2xl" style="
              background-image: radial-gradient(
                circle at left top,
                var(--p-primary-400),
                var(--p-primary-700)
              );
            ">
            <div class="" style="margin: auto; font-size: 2rem; font-weight: bolder">
              Create Program
            </div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label for="programName" class="text-primary-50 font-semibold">Program Name</label>
                <prime_input_text id="programName" class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgram.name" type="text" placeholder="Program name"></prime_input_text>
              </div>
              <div class="inline-flex flex-col gap-2">
                <label for="description" class="text-primary-50 font-semibold">Description</label>
                <prime_textarea id="description" class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgram.description" placeholder="Program description"></prime_textarea>
              </div>
            </div>

            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label for="Program_executable_path" class="text-primary-50 font-semibold">Program Executable
                  Path</label>
                <prime_input_text id="Program_executable_path" class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgram.executable_path" type="text" placeholder="C:/Program Files/VSCode/Code.exe">
                </prime_input_text>
              </div>
              <div class="inline-flex flex-col gap-2">
                <label for="Program_project_path" class="text-primary-50 font-semibold">Open Program In Project
                  Path</label>
                <prime_input_text id="Program_project_path" class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgram.project_path" type="text" placeholder="C:/Users/Hossam/Desktop/project">
                </prime_input_text>
              </div>
            </div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label for="Program_working_directory" class="text-primary-50 font-semibold">Open Program In Working
                  Directory</label>
                <prime_input_text id="Program_working_directory"
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80" v-model="formProgram.working_directory"
                  type="text" placeholder="C:/Users/Hossam/Desktop/project"></prime_input_text>
              </div>
              <div class="inline-flex flex-col gap-2">
                <label for="Program_window_title_pattern" class="text-primary-50 font-semibold">Program Window Title
                  Pattern</label>
                <prime_input_text id="Program_window_title_pattern"
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80" v-model="formProgram.window_title_pattern"
                  type="text" placeholder="Project Name"></prime_input_text>
              </div>
            </div>

            <div class="">
              <input type="file" accept="image/*" @change="onImageChangeProgram" />
            </div>
            <div class="flex items-center gap-4">
              <prime_button label="Cancel" @click="closeCallback" variant="text"
                class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"></prime_button>
              <prime_button label="Create" @click="createProgram" variant="text"
                class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"></prime_button>
            </div>
          </div>
        </template>
      </prime_dialog>
    </div>
    <!-- Edit Program -->
    <div class="card flex justify-center">
      <prime_dialog v-model:visible="editProgramVisible" pt:root:class="!border-0 !bg-transparent"
        pt:mask:class="backdrop-blur-sm">
        <template #container="{ closeCallback }">
          <div class="flex flex-col px-8 py-8 gap-6 rounded-2xl" style="
              background-image: radial-gradient(
                circle at left top,
                var(--p-primary-400),
                var(--p-primary-700)
              );
            ">
            <div class="" style="margin: auto; font-size: 2rem; font-weight: bolder">
              Edit Program
            </div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label for="programName" class="text-primary-50 font-semibold">Program Name</label>
                <prime_input_text id="programName" class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgram.name" type="text" placeholder="Program name"></prime_input_text>
              </div>
              <div class="inline-flex flex-col gap-2">
                <label for="description" class="text-primary-50 font-semibold">Description</label>
                <prime_textarea id="description" class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgram.description" placeholder="Program description"></prime_textarea>
              </div>
            </div>

            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label for="Program_executable_path" class="text-primary-50 font-semibold">Program Executable
                  Path</label>
                <prime_input_text id="Program_executable_path" class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgram.executable_path" type="text" placeholder="C:/Program Files/VSCode/Code.exe">
                </prime_input_text>
              </div>
              <div class="inline-flex flex-col gap-2">
                <label for="Program_project_path" class="text-primary-50 font-semibold">Program Project Path</label>
                <prime_input_text id="Program_project_path" class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgram.project_path" type="text" placeholder="C:/Users/Hossam/Desktop/project">
                </prime_input_text>
              </div>
            </div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label for="Program_working_directory" class="text-primary-50 font-semibold">Program Working
                  Directory</label>
                <prime_input_text id="Program_working_directory"
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80" v-model="formProgram.working_directory"
                  type="text" placeholder="C:/Users/Hossam/Desktop/project"></prime_input_text>
              </div>
              <div class="inline-flex flex-col gap-2">
                <label for="Program_window_title_pattern" class="text-primary-50 font-semibold">Program Window Title
                  Pattern</label>
                <prime_input_text id="Program_window_title_pattern"
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80" v-model="formProgram.window_title_pattern"
                  type="text" placeholder="Project Name"></prime_input_text>
              </div>
            </div>

            <div class="">
              <input type="file" accept="image/*" @change="onImageChangeProgram" />
            </div>
            <div class="flex items-center gap-4">
              <prime_button label="Cancel" @click="closeCallback" variant="text"
                class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"></prime_button>
              <prime_button label="Create" @click="editProgram" variant="text"
                class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"></prime_button>
            </div>
          </div>
        </template>
      </prime_dialog>
    </div>
  </div>
</template>

<script setup>
import { ref,  } from 'vue'

import automationService from '@/services/AutomationService'
// VueFlow



// Toast
import { useToast } from 'primevue/usetoast'
const toast = useToast()
import { useConfirm } from 'primevue/useconfirm'
const confirm = useConfirm()


const emit = defineEmits(['program-selected'])

const selectProgram = async (id) => {
  currentProgramId.value = id
  emit('program-selected', id)
}

// ==============================================
// =================== State ===================
// ==============================================
// 1️⃣
const programs = ref([])
const loadingPrograms = ref(false)
const currentProgramId = ref(null)
const ceateProgramVisible = ref(false)
const editProgramVisible = ref(false)
const formProgram = ref({
  // Text
  name: '',
  description: '',
  executable_path: '',
  project_path: '',
  working_directory: '',
  window_title_pattern: '',
  // global_shortcuts: {},
  // // Boolean
  // is_running: false,
  // // Files & Image
  image: null,
  // is_installed: true,
  // settings: [],
  // env_variables: {},
})
// ==============================================
// ================ 1️⃣ PROGRAMS ================
// ==============================================
// 1️⃣ GET ALL
const loadPrograms = async () => {
  loadingPrograms.value = true
  try {
    const { data } = await automationService.listPrograms()
    programs.value = data
  } catch (error) {
    console.log('Error Programs STORE DATA 👉: ', error)
  } finally {
    loadingPrograms.value = false
    console.log('Programs STORE DATA 👉', programs.value)
  }
}
// 2️⃣ Get Single
const selectProgram = async (id) => {
  if (!id) {
    console.warn('Program ID is missing')
    return
  }

  currentProgramId.value = id
  console.log('selectProgram currentProgramId: ', currentProgramId.value)
  await loadProgram(id)
}
const loadProgram = async (id) => {
  console.log('loadProgram By id: ', id)
  const { data } = await automationService.getProgram(id)
  console.log('loadProgram By id data: ', data)
  currentProgramId.value = data.id
  formProgram.value = {
    name: data.name,
    description: data.description,
    executable_path: data.executable_path,
    project_path: data.project_path,
    working_directory: data.working_directory,
    window_title_pattern: data.window_title_pattern,
    image: null,
  }
}
// 3️⃣ Create Program
const onImageChangeProgram = (e) => {
  formProgram.value.image = e.target.files[0]
}
const createProgram = async () => {
  try {
    const formData = new FormData()

    // ======================
    // Basic Info
    // ======================
    formData.append('name', formProgram.value.name)
    formData.append('description', formProgram.value.description)

    // ======================
    // Execution
    // ======================
    formData.append('executable_path', formProgram.value.executable_path)
    formData.append('project_path', formProgram.value.project_path || '')
    formData.append('working_directory', formProgram.value.working_directory || '')
    formData.append('window_title_pattern', formProgram.value.window_title_pattern || '')

    // // ======================
    // // JSON Fields ⚠️ لازم stringify
    // // ======================
    // formData.append('global_shortcuts', JSON.stringify(JSON.parse(globalShortcutsText.value)))

    // formData.append('env_variables', JSON.stringify(JSON.parse(envVariablesText.value)))

    // // ======================
    // // State
    // // ======================
    // formData.append('is_running', form.value.is_running ? 'true' : 'false')

    // // ======================
    // // Image
    // // ======================
    if (formProgram.value.image) {
      formData.append('image', formProgram.value.image)
    }
    // // =================
    // // JSON
    // // =================
    // formData.append('settings', JSON.stringify(form.value.settings))
    const res = await automationService.createProgram(formData)

    console.log(res.data)
  } catch (error) {
    console.error(error)
    toast.add({
      severity: 'error',
      summary: `❌ Error creating program`,
      detail: `${error.message}`,
      life: 3000,
    })
  } finally {
    ceateProgramVisible.value = false
    console.log('Programs STORE DATA 👉', programs.value)
    toast.add({
      severity: 'success',
      summary: `✅ Program Successfully`,
      detail: `✅ Program Created Successfully`,
      life: 3000,
    })
    await loadPrograms()
  }
}
// 4️⃣ update Program
const openEditProgram = async (id) => {
  if (!id) return

  try {
    // 1️⃣ حدد البرنامج
    currentProgramId.value = id

    // 2️⃣ حمّل بياناته
    await loadProgram(id)

    // 3️⃣ افتح المودال
    editProgramVisible.value = true

    console.log('🟢 Edit Program ID:', id)
  } catch (err) {
    console.error('❌ Failed to open edit program', err)
  }
}
const editProgram = async () => {
  try {
    const formData = new FormData()
    // ======================
    // Basic Info
    // ======================
    formData.append('name', formProgram.value.name)
    formData.append('description', formProgram.value.description)

    // ======================
    // Execution
    // ======================
    formData.append('executable_path', formProgram.value.executable_path)
    formData.append('project_path', formProgram.value.project_path || '')
    formData.append('working_directory', formProgram.value.working_directory || '')
    formData.append('window_title_pattern', formProgram.value.window_title_pattern || '')

    // // ======================
    // // Image
    // // ======================
    if (formProgram.value.image) {
      formData.append('image', formProgram.value.image)
    }

    const res = await automationService.updateProgram(currentProgramId.value, formData)
    console.log('editProgram currentProgramId: ', currentProgramId.value)
    console.log(res.data)
  } catch (errorCode) {
    console.error(errorCode)
    toast.add({
      severity: 'error',
      summary: `❌ Error creating program`,
      detail: `${errorCode.message}`,
      life: 3000,
    })
  } finally {
    editProgramVisible.value = false
    console.log('Programs STORE DATA 👉', programs.value)
    toast.add({
      severity: 'success',
      summary: `✅ Program Successfully`,
      detail: `✅ Program Edit Successfully`,
      life: 3000,
    })
    await loadPrograms()
  }
}
// 5️⃣ Delete Program
const confirmDeleteProgram = (program) => {
  console.log('🗑️ Delete Program:', program)

  confirm.require({
    message: `Are you sure you've deleted the program? "${program.name}"؟`,
    header: '⚠️ Confirm deletion',
    icon: 'pi pi-exclamation-triangle',
    acceptLabel: 'Yes, delete',
    rejectLabel: 'Cancel order',

    accept: async () => {
      await deleteProgram(program.id)
    },

    reject: () => {
      toast.add({
        severity: 'info',
        summary: 'Cancelled',
        detail: 'The program was not deleted',
        life: 2000,
      })
    },
  })
}
const deleteProgram = async (id) => {
  if (!id) return

  try {
    await automationService.deleteProgram(id)
    toast.add({
      severity: 'success',
      summary: '✅ Deleted',
      detail: 'The program was successfully deleted',
      life: 3000,
    })

    // تحديث القائمة
    programs.value = programs.value.filter((p) => p.id !== id)

    // لو البرنامج المحذوف كان محدد
    if (currentProgramId.value === id) {
      currentProgramId.value = null
      formProgram.value = {}
    }
  } catch (err) {
    console.error(err)
    toast.add({
      severity: 'error',
      summary: '❌ mistake',
      detail: 'Program deletion failed',
      life: 3000,
    })
  }
}
// 6️⃣ Open Program
const openProgram = async (programId) => {
  await automationService.openProgram(programId) // 🚀 فتح البرنامج
}
// 7️⃣ Close Program
const closeProgram = async (programId) => {
  await automationService.closeProgram(programId) // ❌ غلق البرنامج
}
// 8️⃣ Status Program
const statusProgram = async (programId) => {
  const { data } = await automationService.statusProgram(programId) // ℹ️ حالة البرنامج
  return data
}

const focusProgram = async (programId) => {
  try {
    const { data } = await automationService.focusProgram(programId)
    console.log('data: ', data)
    toast.add({
      severity: 'success',
      summary: '✅ Focused',
      detail: `Program focused successfully`,
      life: 2000,
    })
  } catch (err) {
    console.error(err)
    toast.add({
      severity: 'error',
      summary: '❌ Focus failed',
      detail: err.message,
      life: 3000,
    })
  }
}

const maximizeProgram = async (programId) => {
  try {
    const { data } = await automationService.maximizeProgram(programId)
    console.log('data: ', data)

    toast.add({
      severity: 'success',
      summary: '✅ Maximized',
      detail: `Program maximized successfully`,
      life: 2000,
    })
  } catch (err) {
    console.error(err)
    toast.add({
      severity: 'error',
      summary: '❌ Maximize failed',
      detail: err.message,
      life: 3000,
    })
  }
}


</script>

<style scoped>
.programs-page {
  max-width: 900px;
  margin: auto;
}
</style>
