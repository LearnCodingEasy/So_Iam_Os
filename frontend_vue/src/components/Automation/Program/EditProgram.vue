<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  visible: Boolean,
  program: Object,
})

const emit = defineEmits(['update:visible', 'save'])

const editProgramVisible = ref(false)

const formProgram = ref({
  name: '',
  description: '',
  executable_path: '',
  project_path: '',
  working_directory: '',
  window_title_pattern: '',
  image: null,
})

watch(
  () => props.visible,
  (v) => {
    editProgramVisible.value = v
  },
)

watch(
  () => props.program,
  (program) => {
    if (program) {
      formProgram.value = { ...program }
    }
  },
  { immediate: true },
)

const onImageChangeProgram = (e) => {
  formProgram.value.image = e.target.files[0]
}

const saveProgram = () => {
  emit('save', formProgram.value)
  emit('update:visible', false)
}
</script>

<template>
  <div class="card flex justify-center">
    <prime_dialog
      v-model:visible="editProgramVisible"
      pt:root:class="!border-0 !bg-transparent"
      pt:mask:class="backdrop-blur-sm"
    >
      <template #container="{ closeCallback }">
        <div
          class="flex flex-col px-8 py-8 gap-6 rounded-2xl"
          style="
            background-image: radial-gradient(
              circle at left top,
              var(--p-primary-400),
              var(--p-primary-700)
            );
          "
        س>
          <div class="title">Edit Program</div>

          <!-- name + description -->

          <div class="inline-flex flex-row gap-2">
            <div class="field">
              <label>Program Name</label>
              <prime_input_text v-model="formProgram.name" placeholder="Program name" />
            </div>

            <div class="field">
              <label>Description</label>
              <prime_textarea v-model="formProgram.description" placeholder="Program description" />
            </div>
          </div>

          <!-- paths -->

          <div class="inline-flex flex-row gap-2">
            <div class="field">
              <label>Executable Path</label>
              <prime_input_text v-model="formProgram.executable_path" />
            </div>

            <div class="field">
              <label>Project Path</label>
              <prime_input_text v-model="formProgram.project_path" />
            </div>
          </div>

          <!-- more -->

          <div class="inline-flex flex-row gap-2">
            <div class="field">
              <label>Working Directory</label>
              <prime_input_text v-model="formProgram.working_directory" />
            </div>

            <div class="field">
              <label>Window Title Pattern</label>
              <prime_input_text v-model="formProgram.window_title_pattern" />
            </div>
          </div>

          <!-- image -->

          <input type="file" accept="image/*" @change="onImageChangeProgram" />

          <!-- buttons -->

          <div class="flex gap-4">
            <prime_button label="Cancel" @click="emit('update:visible', false)" />

            <prime_button label="Save" @click="saveProgram" />
          </div>
        </div>
      </template>
    </prime_dialog>
  </div>
</template>

<!--
<div class="card flex justify-center">
      <prime_dialog
        v-model:visible="editProgramVisible"
        pt:root:class="!border-0 !bg-transparent"
        pt:mask:class="backdrop-blur-sm"
      >
        <template #container="{ closeCallback }">
          <div
            class="flex flex-col px-8 py-8 gap-6 rounded-2xl"
            style="
              background-image: radial-gradient(
                circle at left top,
                var(--p-primary-400),
                var(--p-primary-700)
              );
            "
          >
            <div class="" style="margin: auto; font-size: 2rem; font-weight: bolder">
              Edit Program
            </div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label for="programName" class="text-primary-50 font-semibold">Program Name</label>
                <prime_input_text
                  id="programName"
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgram.name"
                  type="text"
                  placeholder="Program name"
                ></prime_input_text>
              </div>
              <div class="inline-flex flex-col gap-2">
                <label for="description" class="text-primary-50 font-semibold">Description</label>
                <prime_textarea
                  id="description"
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgram.description"
                  placeholder="Program description"
                ></prime_textarea>
              </div>
            </div>

            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label for="Program_executable_path" class="text-primary-50 font-semibold"
                  >Program Executable Path</label
                >
                <prime_input_text
                  id="Program_executable_path"
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgram.executable_path"
                  type="text"
                  placeholder="C:/Program Files/VSCode/Code.exe"
                >
                </prime_input_text>
              </div>
              <div class="inline-flex flex-col gap-2">
                <label for="Program_project_path" class="text-primary-50 font-semibold"
                  >Program Project Path</label
                >
                <prime_input_text
                  id="Program_project_path"
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgram.project_path"
                  type="text"
                  placeholder="C:/Users/Hossam/Desktop/project"
                >
                </prime_input_text>
              </div>
            </div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label for="Program_working_directory" class="text-primary-50 font-semibold"
                  >Program Working Directory</label
                >
                <prime_input_text
                  id="Program_working_directory"
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgram.working_directory"
                  type="text"
                  placeholder="C:/Users/Hossam/Desktop/project"
                ></prime_input_text>
              </div>
              <div class="inline-flex flex-col gap-2">
                <label for="Program_window_title_pattern" class="text-primary-50 font-semibold"
                  >Program Window Title Pattern</label
                >
                <prime_input_text
                  id="Program_window_title_pattern"
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgram.window_title_pattern"
                  type="text"
                  placeholder="Project Name"
                ></prime_input_text>
              </div>
            </div>

            <div class="">
              <input type="file" accept="image/*" @change="onImageChangeProgram" />
            </div>
            <div class="flex items-center gap-4">
              <prime_button
                label="Cancel"
                @click="closeCallback"
                variant="text"
                class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"
              ></prime_button>
              <prime_button
                label="Create"
                @click="editProgram"
                variant="text"
                class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"
              ></prime_button>
            </div>
          </div>
        </template>
      </prime_dialog>
    </div>
-->
