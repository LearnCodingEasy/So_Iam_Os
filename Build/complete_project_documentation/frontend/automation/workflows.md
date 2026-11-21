# automation workflows

## Routed screens and source evidence

- Route /automation (automation) is declared at router/index.js:L261; metadata: requiresAuth.
- Route /automation_Dashboard (automation_Dashboard) is declared at router/index.js:L267; metadata: requiresAuth.
- Route /automation_ProgramList (automation_ProgramList) is declared at router/index.js:L273; metadata: requiresAuth.
- Route /automation_programs_create (automation_programs_create) is declared at router/index.js:L279; metadata: requiresAuth.
- Route /automation/:id (automation_programs_edit) is declared at router/index.js:L285; metadata: requiresAuth.
- Route /automation_TaskCreate (automation_TaskCreate) is declared at router/index.js:L291; metadata: requiresAuth.
- Route /automation_TaskEditor (automation_TaskEditor) is declared at router/index.js:L297; metadata: requiresAuth.

### views/automation/AutomationView.vue
import { ref, reactive, watch, onMounted, onUnmounted } from 'vue'
import { useVueFlow } from '@vue-flow/core'
import { debounce } from 'lodash'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
import { useProgramStore } from '@/stores/automation/useProgramStore'
import { useProgramElementStore } from '@/stores/automation/useProgramElementStore'
import { useWorkflowStore } from '@/stores/automation/useWorkflowStore'
import { useTaskStore } from '@/stores/automation/useTaskStore'
import automationService from '@/services/Automation/AutomationService'
import { useApiTracker } from '@/composables/useApiTracker'
import NodeMarketplace from '@/components/automation/Node/NodeMarketplace.vue'

### views/automation/DashboardAutomationView.vue
import { ref, onMounted } from 'vue'
import taskService from '../../services/Automation/taskService'

### views/automation/icon.vue
No static import lines detected.

### views/automation/ProgramCreate.vue
import { ref } from 'vue'
import programService from '@/services/Automation/AutomationService'

### views/automation/ProgramEdit.vue
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import programService from '@/services/Automation/AutomationService'

### views/automation/ProgramList.vue
import { ref, onMounted } from 'vue'
import programService from '../../services/Automation/AutomationService'

### views/automation/TaskCreate.vue
import { ref, onMounted } from 'vue'
import api from '../../services/Shared/api'

### views/automation/TaskEditor.vue
import { ref, onMounted } from 'vue'
import api from '../../services/Shared/api'
import { useRoute } from 'vue-router'


**UNKNOWN:** End-to-end transitions and error outcomes are not runtime verified.
