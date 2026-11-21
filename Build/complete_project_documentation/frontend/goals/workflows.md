# goals workflows

## Routed screens and source evidence

- Route /goals (goals) is declared at router/index.js:L146; metadata: requiresAuth.

### views/goals/Goals.vue
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { useGoalsStore } from '@/stores/goals/goalsStore'
import { useAppToast } from '@/composables/useAppToast'
import * as goalApi from '@/services/Goals/goals'
import { createTask, listTasks } from '@/services/Tasks/tasks'
import { getLearningGoals } from '@/services/Learning/learning'
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { useGoalsStore } from '@/stores/goals/goalsStore'
import { useAppToast } from '@/composables/useAppToast'
import * as goalApi from '@/services/Goals/goals'
import { createTask, listTasks } from '@/services/Tasks/tasks'
import { getLearningGoals } from '@/services/Learning/learning'


**UNKNOWN:** End-to-end transitions and error outcomes are not runtime verified.
