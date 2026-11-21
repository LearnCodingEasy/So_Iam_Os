# notifications workflows

## Routed screens and source evidence

- Route /notifications (notifications) is declared at router/index.js:L200; metadata: requiresAuth.

### views/notifications/NotificationsView.vue
import { onMounted, ref } from 'vue'
import { listNotifications, markAllRead, markRead, archiveNotification } from '@/services/Notifications/notifications'


**UNKNOWN:** End-to-end transitions and error outcomes are not runtime verified.
