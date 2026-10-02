<script setup>
// ==================================================
// 📦 Props & Emits
// ==================================================
const props = defineProps({
  visible: { type: Boolean, required: true },
  form: { type: Object, required: true },
})

const emit = defineEmits(['update:visible', 'image-change', 'submit'])
</script>

<template>
  <div class="card flex justify-center">
    <prime_dialog
      :visible="visible"
      @update:visible="emit('update:visible', $event)"
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
          <!-- Title -->
          <div style="margin: auto; font-size: 2rem; font-weight: bolder">Create Program</div>

          <!-- Name & Description -->
          <div class="inline-flex flex-row gap-2">
            <div class="inline-flex flex-col gap-2">
              <label for="programName" class="text-primary-50 font-semibold">Program Name</label>
              <prime_input_text
                id="programName"
                class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                :value="form?.name"
                @input="form.name = $event.target.value"
                type="text"
                placeholder="Program name"
              />
            </div>
            <div class="inline-flex flex-col gap-2">
              <label for="description" class="text-primary-50 font-semibold">Description</label>
              <prime_textarea
                id="description"
                class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                :value="form.description"
                @input="form.description = $event.target.value"
                placeholder="Program description"
              />
            </div>
          </div>

          <!-- Executable Path & Project Path -->
          <div class="inline-flex flex-row gap-2">
            <div class="inline-flex flex-col gap-2">
              <label for="executable_path" class="text-primary-50 font-semibold"
                >Executable Path</label
              >
              <prime_input_text
                id="executable_path"
                class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                :value="form.executable_path"
                @input="form.executable_path = $event.target.value"
                placeholder="C:/Program Files/VSCode/Code.exe"
              />
            </div>
            <div class="inline-flex flex-col gap-2">
              <label for="project_path" class="text-primary-50 font-semibold">Project Path</label>
              <prime_input_text
                id="project_path"
                class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                :value="form.project_path"
                @input="form.project_path = $event.target.value"
                placeholder="C:/Users/Hossam/Desktop/project"
              />
            </div>
          </div>

          <!-- Working Directory & Window Title -->
          <div class="inline-flex flex-row gap-2">
            <div class="inline-flex flex-col gap-2">
              <label for="working_directory" class="text-primary-50 font-semibold"
                >Working Directory</label
              >
              <prime_input_text
                id="working_directory"
                class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                :value="form.working_directory"
                @input="form.working_directory = $event.target.value"
                placeholder="C:/Users/Hossam/Desktop/project"
              />
            </div>
            <div class="inline-flex flex-col gap-2">
              <label for="window_title_pattern" class="text-primary-50 font-semibold"
                >Window Title Pattern</label
              >
              <prime_input_text
                id="window_title_pattern"
                class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                :value="form.window_title_pattern"
                @input="form.window_title_pattern = $event.target.value"
                placeholder="Project Name"
              />
            </div>
          </div>

          <!-- Image -->
          <div>
            <input type="file" accept="image/*" @change="emit('image-change', $event)" />
          </div>

          <!-- Actions -->
          <div class="flex items-center gap-4">
            <prime_button
              label="Cancel"
              @click="closeCallback"
              variant="text"
              class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"
            />
            <prime_button
              label="Create"
              @click="emit('submit')"
              variant="text"
              class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"
            />
          </div>
        </div>
      </template>
    </prime_dialog>
  </div>

</template>
<!-- <div class="card flex justify-center">

      <prime_dialog
        v-model:visible="ceateProgramVisible"
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
              Create Program
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
                  >Open Program In Project Path</label
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
                  >Open Program In Working Directory</label
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
                @click="createProgram"
                variant="text"
                class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"
              ></prime_button>
            </div>
          </div>
        </template>
      </prime_dialog>
    </div> -->
