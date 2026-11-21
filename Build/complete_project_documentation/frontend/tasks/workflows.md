# tasks workflows

## Routed screens and source evidence

- Route /tasks/today (today-tasks) is declared at router/index.js:L152; metadata: requiresAuth.
- Route /tasks (tasks) is declared at router/index.js:L176; metadata: requiresAuth.

### views/tasks/TasksCalendar copy.vue
import { computed, onMounted, ref } from 'vue'
import { listTasks, createTask, updateTask, completeTask } from '@/services/Tasks/tasks'
import api from '@/services/Shared/api'
import { endpoints } from '@/services/Shared/endpoints'

### views/tasks/TasksCalendar.vue
import { ref, computed, onMounted, watch } from 'vue'
import {

### views/tasks/TodayTasks.vue
import { computed, onMounted, reactive, ref } from 'vue'
import {


**UNKNOWN:** End-to-end transitions and error outcomes are not runtime verified.
