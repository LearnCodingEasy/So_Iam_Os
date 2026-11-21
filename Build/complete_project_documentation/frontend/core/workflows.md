# core workflows

## Routed screens and source evidence

- Route /progress (progress) is declared at router/index.js:L158; metadata: requiresAuth.
- Route /system/frontend (frontend-enhancements) is declared at router/index.js:L210; metadata: requiresAuth.
- Route /settings (settings) is declared at router/index.js:L220; metadata: requiresAuth.
- Route /dashboard (dashboard) is declared at router/index.js:L252; metadata: requiresAuth.

### views/core/DashboardView.vue
import { ref, computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useOnline, useDark } from '@vueuse/core'
import { toast } from 'vue-sonner'
import { dashboardService } from '@/services/Core/dashboard'
import {
import { Line } from 'vue-chartjs'

### views/core/MyProgress.vue
import { onMounted, ref } from 'vue'
import { useAppToast } from '@/composables/useAppToast'
import { getApiErrorMessage } from '@/utils/apiError'
import api from '@/services/Shared/api'

### views/core/Settings.vue
import { onMounted, reactive, ref, watch } from 'vue'
import api from '@/services/Shared/api'
import Button from 'primevue/button'
import Card from 'primevue/card'
import Select from 'primevue/select'
import Checkbox from 'primevue/checkbox'
import InputNumber from 'primevue/inputnumber'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Tag from 'primevue/tag'
import Password from 'primevue/password'
import InputText from 'primevue/inputtext'


**UNKNOWN:** End-to-end transitions and error outcomes are not runtime verified.
