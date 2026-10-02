<template>
  <div class="p-6 max-w-6xl mx-auto">
    <h1 class="text-2xl font-bold mb-6">Edite Program</h1>
    <div class="grid gap-4">
      <div class="name_description">
        <div>
          <label class="block font-semibold mb-1">Name</label>
          <input v-model="form.name" type="text" class="input" placeholder="Program name" />
        </div>
        <div>
          <label class="block font-semibold mb-1">Description</label>
          <textarea
            v-model="form.description"
            placeholder="Program description"
            name=""
            id=""
            class="textarea"
            cols="30"
            rows="3"
          ></textarea>
        </div>
      </div>
      <div class="executable_path_project_path">
        <div>
          <label class="block font-semibold mb-1">Executable Path</label>
          <input
            v-model="form.executable_path"
            type="text"
            class="input"
            placeholder="C:/Program Files/VSCode/Code.exe"
          />
        </div>
        <div>
          <label class="block font-semibold mb-1">Project Path (optional)</label>
          <input
            v-model="form.project_path"
            type="text"
            class="input"
            placeholder="C:/Users/Hossam/Desktop/project"
          />
        </div>
      </div>
      <div class="working_directory_window_title_pattern">
        <div>
          <label class="block font-semibold mb-1">Working Directory (optional)</label>
          <input
            v-model="form.working_directory"
            type="text"
            class="input"
            placeholder="C:/Users/Hossam/Desktop/project"
          />
        </div>
        <div>
          <label class="block font-semibold mb-1">window title pattern (optional)</label>
          <input
            v-model="form.window_title_pattern"
            type="text"
            class="input"
            placeholder="Project Name"
          />
        </div>
      </div>
      <input type="file" accept="image/*" @change="onImageChange" />
      <!--

      <div>
        <label class="block font-semibold mb-1">Global Shortcuts (JSON)</label>
        <textarea
          v-model="globalShortcutsText"
          rows="6"
          class="textarea"
          placeholder='{"theme": "dark", "autosave": true}'
        ></textarea>
      </div>



      <div>
        <label class="block font-semibold mb-1">is_running</label>
        <input
          v-model="form.is_running"
          type="checkbox"
          class="input"
          placeholder="C:/Users/Hossam/Desktop/project"
        />
      </div>
      <div class="new_data">
        <label>settings [press alt + comma to add]:</label><br />
        <input
          type="text"
          v-model="tempSetting"
          @keyup.alt="addSetting"
          placeholder="Your Settings"
          class="w-full mt-2 py-2 px-4 border border-gray-200 rounded-lg"
        />
        <div class="grid_12 mt-4">
          <div class="">
            <span @click="deleteSetting(setting)" class="cursor-pointer">
              <prime_tag
                severity="success"
                v-for="setting in form.settings"
                :key="setting"
                class="mr-1"
              >
                <span @click="deleteSetting(setting)" class="item_1">
                  <prime_tag severity="success" :value="setting"> </prime_tag>
                </span>
              </prime_tag>
            </span>
          </div>
        </div>
      </div>

       <div>
        <label class="block font-semibold mb-1">env_variables (JSON)</label>
        <textarea
          v-model="envVariablesText"
          rows="6"
          class="textarea"
          placeholder='{"theme": "dark", "autosave": true}'
        ></textarea>
      </div>
      -->

      <button @click="createProgram" class="btn-primary">Create Program</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
// import { useRoute, useRouter } from 'vue-router'
import programService from '@/services/AutomationService'

// =======================
// Router
// =======================
const route = useRoute()
// const router = useRouter()

// =======================
// State
// =======================
const currentId = ref(null)

// =======================
// State
// =======================
const form = ref({
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
// const tempSetting = ref('')

// const globalShortcutsText = ref('{}')
// const envVariablesText = ref('{}')

// =======================
// Images
// =======================
const onImageChange = (e) => {
  form.value.image = e.target.files[0]
}
// =======================
// Json
// =======================
// const addSetting = (event) => {
//   if (event.key === ',' && tempSetting.value.trim() !== '') {
//     if (!form.value.settings.includes(tempSetting.value)) {
//       form.value.settings.push(tempSetting.value)
//     }
//     tempSetting.value = ''
//   }
// }
// const deleteSetting = (setting) => {
//   form.value.settings = form.value.settings.filter((item) => {
//     return setting !== item
//   })
// }
// =======================
// API
// =======================
const createProgram = async () => {
  try {
    const formData = new FormData()

    // ======================
    // Basic Info
    // ======================
    formData.append('name', form.value.name)
    formData.append('description', form.value.description)

    // ======================
    // Execution
    // ======================
    formData.append('executable_path', form.value.executable_path)
    formData.append('project_path', form.value.project_path || '')
    formData.append('working_directory', form.value.working_directory || '')
    formData.append('window_title_pattern', form.value.window_title_pattern || '')

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
    if (form.value.image) {
      formData.append('image', form.value.image)
    }
    // // =================
    // // JSON
    // // =================
    // formData.append('settings', JSON.stringify(form.value.settings))
    const res = await programService.createProgram(formData)
    alert('✅ Program created successfully')
    console.log(res.data)
  } catch (err) {
    alert('❌ Error creating program')
    console.error(err)
  }
}

// =======================
// Get Explain By ID
// =======================
const getExplain = async () => {
  try {
    currentId.value = route.params.id
    const res = await programService.get(currentId.value)
    form.value.name = res.data.name

    form.value.description = res.data.description
    form.value.email = res.data.email
    form.value.url = res.data.url
    form.value.price = res.data.price
    form.value.count = res.data.count
    form.value.views = res.data.views
    form.value.rating = res.data.rating
    form.value.actual_price = res.data.actual_price
    form.value.is_active = res.data.is_active
    form.value.birth_date = res.data.birth_date
    form.value.start_time = res.data.start_time
  } catch (err) {
    console.log('Get error:', err)
  }
}

// =======================
// Lifecycle
// =======================
onMounted(() => {
  getExplain()
})
</script>

<style scoped>
.input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 6px;
}
.textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 6px;
}
.btn-primary {
  padding: 10px 20px;
  background: #2563eb;
  color: white;
  border-radius: 6px;
}
.name_description {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(49%, 1fr));
}
.executable_path_project_path {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(49%, 1fr));
}
</style>
