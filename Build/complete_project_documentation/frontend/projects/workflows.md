# projects workflows

## Routed screens and source evidence

- Route /projects (projects) is declared at router/index.js:L183; metadata: requiresAuth.

### views/projects/ProjectsView.vue
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { useProjectsStore } from '@/stores/projects/projects'
import Card from 'primevue/card'
import Button from 'primevue/button'
import Column from 'primevue/column'
import DataTable from 'primevue/datatable'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import Textarea from 'primevue/textarea'
import Select from 'primevue/select'
import Tag from 'primevue/tag'
import Message from 'primevue/message'


**UNKNOWN:** End-to-end transitions and error outcomes are not runtime verified.
