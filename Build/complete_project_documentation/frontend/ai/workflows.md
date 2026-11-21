# ai workflows

## Routed screens and source evidence

- Route /ai/agents (ai-agents) is declared at router/index.js:L193; metadata: requiresAuth.
- Route /ai (ai-chat) is declared at router/index.js:L230; metadata: requiresAuth.
- Route /ai/control (ai-control) is declared at router/index.js:L236; metadata: requiresAuth.
- Route /ai/operations (ai-operations) is declared at router/index.js:L242; metadata: requiresAuth.

### views/ai/AgentPlanner.vue
import { computed, reactive, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import Button from 'primevue/button'
import Card from 'primevue/card'
import Textarea from 'primevue/textarea'
import InputText from 'primevue/inputtext'
import Select from 'primevue/select'
import Message from 'primevue/message'
import Tag from 'primevue/tag'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import aiControl from '@/services/AI/aiControl'

### views/ai/AI.vue
import { computed, onMounted, ref } from 'vue'
import Button from 'primevue/button'
import Card from 'primevue/card'
import Message from 'primevue/message'
import Password from 'primevue/password'
import Select from 'primevue/select'
import Tag from 'primevue/tag'
import Textarea from 'primevue/textarea'
import { sendMessage } from '@/services/AI/Ai'
import {

### views/ai/AIChat.vue
import { computed, defineComponent, h, onMounted, reactive, ref, nextTick } from 'vue'
import aiControl from '@/services/AI/aiControl'
import { sendMessage as sendNonStreamingMessage, streamMessage } from '@/services/AI/Ai'
import MarkdownRenderer from '@/components/ai/MarkdownRenderer.vue'
import { useI18n } from 'vue-i18n'

### views/ai/AIControl.vue
import { computed, onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { gsap } from 'gsap'
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import { z } from 'zod'
import NProgress from 'nprogress'
import Button from 'primevue/button'
import Card from 'primevue/card'
import Message from 'primevue/message'
import Password from 'primevue/password'
import Select from 'primevue/select'

### views/ai/AIOperationsView.vue
import { onMounted, reactive, ref } from 'vue'
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { storeToRefs } from 'pinia'
import Button from 'primevue/button'
import Card from 'primevue/card'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Tabs from 'primevue/tabs'
import TabList from 'primevue/tablist'
import Tab from 'primevue/tab'
import TabPanels from 'primevue/tabpanels'


**UNKNOWN:** End-to-end transitions and error outcomes are not runtime verified.
