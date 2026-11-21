<template>
  <div class="ai-markdown" v-html="safeHtml" />
</template>

<script setup>
import { computed } from 'vue'
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import Prism from 'prismjs'
import 'prismjs/components/prism-markup'
import 'prismjs/components/prism-javascript'
import 'prismjs/components/prism-python'
import 'prismjs/components/prism-json'
import 'prismjs/components/prism-bash'
import 'prismjs/themes/prism.css'

const props = defineProps({ content: { type: String, default: '' } })
marked.setOptions({ gfm: true, breaks: true })

const safeHtml = computed(() => {
  const html = marked.parse(props.content || '')
  const sanitized = DOMPurify.sanitize(html, {
    USE_PROFILES: { html: true },
    ADD_ATTR: ['target', 'rel'],
  })
  const wrapper = document.createElement('div')
  wrapper.innerHTML = sanitized
  wrapper.querySelectorAll('pre code').forEach((block) => {
    const language = [...block.classList].find((name) => name.startsWith('language-'))?.slice(9)
    if (language && Prism.languages[language]) {
      block.innerHTML = Prism.highlight(block.textContent || '', Prism.languages[language], language)
    }
  })
  wrapper.querySelectorAll('a').forEach((link) => {
    link.setAttribute('target', '_blank')
    link.setAttribute('rel', 'noopener noreferrer')
  })
  return wrapper.innerHTML
})
</script>

<style scoped>
.ai-markdown :deep(pre) { overflow: auto; border-radius: 12px; padding: 1rem; }
.ai-markdown :deep(code) { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
.ai-markdown :deep(table) { width: 100%; border-collapse: collapse; }
.ai-markdown :deep(th), .ai-markdown :deep(td) { padding: .55rem .7rem; border: 1px solid var(--p-content-border-color); text-align: start; }
</style>
