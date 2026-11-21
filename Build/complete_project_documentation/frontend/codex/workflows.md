# codex workflows

## Routed screens and source evidence

- Route /codex (codex) is declared at router/index.js:L182; metadata: requiresAuth.

### views/codex/CodexBuildWorkspace.vue
import { computed, onMounted, ref } from 'vue'
import { VueFlow } from '@vue-flow/core'
import { Background } from '@vue-flow/background'
import { Controls } from '@vue-flow/controls'
import { MiniMap } from '@vue-flow/minimap'
import Button from 'primevue/button'
import Tag from 'primevue/tag'
import Message from 'primevue/message'
import codex from '@/services/Codex/codex'
import '@vue-flow/core/dist/style.css'
import '@vue-flow/core/dist/theme-default.css'

### views/codex/CodexCapabilities.spec.js
import { beforeEach, describe, expect, it } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useCodexStore } from '@/stores/codex/codex'

### views/codex/CodexCapabilities.vue
import { computed, onMounted, ref } from 'vue'
import Card from 'primevue/card'
import Button from 'primevue/button'
import Tag from 'primevue/tag'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import InputText from 'primevue/inputtext'
import ProgressBar from 'primevue/progressbar'
import Message from 'primevue/message'
import Dialog from 'primevue/dialog'
import { useCodexStore } from '@/stores/codex/codex'
import codex from '@/services/Codex/codex'

### views/codex/CodexView.vue
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useCodexStore } from '@/stores/codex/codex'
import codex from '@/services/Codex/codex'
import CodexSidebar from '@/components/codex/Layout/CodexSidebar.vue'
import CodexRightSidebar from '@/components/codex/Layout/CodexRightSidebar.vue'
import CodexTopbar from '@/components/codex/Layout/CodexTopbar.vue'
import CodexChatPanel from '@/components/codex/panels/CodexChatPanel.vue'
import CodexAnalysisPanel from '@/components/codex/panels/CodexAnalysisPanel.vue'
import CodexPipelinePanel from '@/components/codex/panels/CodexPipelinePanel.vue'
import CodexGovernancePanel from '@/components/codex/panels/CodexGovernancePanel.vue'
import CodexRegistryPanel from '@/components/codex/panels/CodexRegistryPanel.vue'


**UNKNOWN:** End-to-end transitions and error outcomes are not runtime verified.
