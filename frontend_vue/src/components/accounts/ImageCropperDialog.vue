<template>
  <Dialog
    v-model:visible="visible"
    modal
    header="تعديل الصورة"
    :style="{ width: 'min(92vw, 720px)' }"
    @hide="cleanup"
  >
    <div class="cropper-shell">
      <img ref="imageRef" :src="previewUrl" alt="Preview" class="cropper-image" />
    </div>
    <template #footer>
      <Button label="إلغاء" text @click="visible = false" /><Button
        label="اعتماد القص"
        icon="pi pi-check"
        :disabled="!cropper"
        @click="crop"
      />
    </template>
  </Dialog>
</template>
<script setup>
import { nextTick, onBeforeUnmount, ref, watch } from 'vue'
import Dialog from 'primevue/dialog'
import Button from 'primevue/button'
import Cropper from 'cropperjs'
import 'cropperjs/dist/cropper.css'
const props = defineProps({
  file: { type: [File, Object], default: null },
  aspectRatio: { type: Number, default: 1 },
})
const emit = defineEmits(['cropped', 'cancel'])
const visible = ref(false),
  previewUrl = ref(''),
  imageRef = ref(null),
  cropper = ref(null)
let objectUrl = ''
watch(
  () => props.file,
  async (file) => {
    if (!file) return
    cleanup(false)
    objectUrl = URL.createObjectURL(file)
    previewUrl.value = objectUrl
    visible.value = true
    await nextTick()
    cropper.value = new Cropper(imageRef.value, {
      aspectRatio: props.aspectRatio,
      viewMode: 1,
      autoCropArea: 1,
      responsive: true,
    })
  },
)
function crop() {
  const canvas = cropper.value?.getCroppedCanvas({ maxWidth: 1200, maxHeight: 1200 })
  if (!canvas) return
  canvas.toBlob(
    (blob) => {
      if (!blob) return
      emit(
        'cropped',
        new File([blob], props.file?.name || 'cropped-image.jpg', {
          type: blob.type || 'image/jpeg',
        }),
      )
      visible.value = false
    },
    'image/jpeg',
    0.9,
  )
}
function cleanup(emitCancel = true) {
  cropper.value?.destroy()
  cropper.value = null
  if (objectUrl) URL.revokeObjectURL(objectUrl)
  objectUrl = ''
  previewUrl.value = ''
  if (emitCancel && visible.value) emit('cancel')
}
onBeforeUnmount(() => cleanup(false))
</script>
<style scoped>
.cropper-shell {
  min-height: 320px;
  max-height: 65vh;
  overflow: hidden;
  background: var(--p-content-hover-background);
  border-radius: 12px;
}
.cropper-image {
  display: block;
  max-width: 100%;
  max-height: 65vh;
}
</style>
