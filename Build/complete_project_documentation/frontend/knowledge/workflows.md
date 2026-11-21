# knowledge workflows

## Routed screens and source evidence

- Route /knowledge (knowledge) is declared at router/index.js:L115; metadata: requiresAuth.

### views/knowledge/knowledgeView.vue
import { computed, onMounted, ref } from 'vue'
import {
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { storeToRefs } from 'pinia'
import { useKnowledgeStore } from '@/stores/knowledge/knowledgeStore'
import KnowledgeCard from '@/components/knowledge/KnowledgeCard.vue'
import KnowledgeEmptyState from '@/components/knowledge/KnowledgeEmptyState.vue'
import KnowledgeForm from '@/components/knowledge/KnowledgeForm.vue'


**UNKNOWN:** End-to-end transitions and error outcomes are not runtime verified.
