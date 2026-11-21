# shared workflows

## Routed screens and source evidence

- Route / (home) is declared at router/index.js:L60; metadata: requiresAuth.
- Route /About (About) is declared at router/index.js:L69; metadata: requiresAuth.
- Route /:catchAll(.*) (NotFound) is declared at router/index.js:L307; metadata: catchall.

### views/shared/AboutView.vue
import { ref, onMounted } from 'vue'
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { useWebSocket } from '@vueuse/core'
import { z } from 'zod'

### views/shared/HomeView.vue
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { RouterLink } from 'vue-router'
import { dashboardService } from '@/services/Core/dashboard'

### views/shared/Page_Not_Found.vue
No static import lines detected.


**UNKNOWN:** End-to-end transitions and error outcomes are not runtime verified.
