# accounts workflows

## Routed screens and source evidence

- Route /login (login) is declared at router/index.js:L82; metadata: requiresGuest.
- Route /auth-callback (AuthCallback) is declared at router/index.js:L92; metadata: callback route has no guard metadata.
- Route /profile/:id (profile) is declared at router/index.js:L102; metadata: requiresAuth.

### views/accounts/auth-callback.vue
import api from '@/services/Shared/api'

### views/accounts/AuthCallback.vue
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/accounts/user'
import axios from 'axios'

### views/accounts/LoginView.vue
import LoginForm from '@/components/accounts/LoginForm.vue'
import SignupForm from '@/components/accounts/SignupForm.vue'

### views/accounts/ProfileView.vue
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '@/stores/accounts/user'
import { usersAccountsAPI } from '@/services/Accounts/usersAccounts'
import ImageCropperDialog from '@/components/accounts/ImageCropperDialog.vue'
import fallbackImage from '@/assets/Images/Page_Not_Found/404.jpg'


**UNKNOWN:** End-to-end transitions and error outcomes are not runtime verified.
